"""Redirect middleware for Django CMS."""
from __future__ import absolute_import

import re
import sys

if sys.version_info >= (3, 0):
    from urllib.parse import urlparse
if sys.version_info < (3, 0) and sys.version_info >= (2, 5):
    from urlparse import urlparse

from cms_redirects.models import CMSRedirect
from django import http
from django.conf import settings


I18N_RE = re.compile(r'^/[a-zA-Z][a-zA-Z]')


def trailing_slash(path, path_list):
    # Sometimes people define urls without the trailing slash when
    # settings.APPEND_SLASH is True.
    if settings.APPEND_SLASH and path.endswith('/'):
        path_list.append(path[:-1])


def i18n_prefix(path, path_list):
    # if /en (or whatever) gets prepended to the path, it gets done
    # before this executes, so we need to check for duplicates here
    if settings.USE_I18N and I18N_RE.match(path):
        path_list.append(path[3:])


class RedirectMiddleware(object):
    """Middleware for handling redirects."""

    def add_path_variations(self, path_list, variation_fn):
        # for transformations, we want to apply them to each of the possible
        # outcomes we've already generated, so iterate through the list and
        # apply the function to each.

        # As we are appending to the list we are iterating over, iterate over
        # a copy of the list to avoid an endless loop - the [:] does the copy
        for path in path_list[:]:
            variation_fn(path, path_list)

    def get_possible_paths(self, parsed_path):
        """Get a list of possible url paths to look for."""
        # Get the usable url parts
        path = parsed_path.path

        # We'll always lookup the exact path
        possible_paths = [path]

        self.add_path_variations(possible_paths, trailing_slash)
        self.add_path_variations(possible_paths, i18n_prefix)

        return possible_paths

    def get_query(self, parsed_path):
        """Get and format query parameters."""
        if parsed_path.query:
            query = parsed_path.query
        else:
            query = ''

        return query

    def get_cms_redirect(self, possible_paths):
        """Get the latest redirect for the specified path."""
        try:
            redirect = CMSRedirect.objects.filter(
                site__id__exact=settings.SITE_ID,
                old_path__in=possible_paths
            ).latest('pk')
        except CMSRedirect.DoesNotExist:
            redirect = None
        return redirect

    def get_cms_redirect_response_class(self, redirect):
        """Get the appropriate redirect class."""
        if int(redirect.response_code) == 302:
            return http.HttpResponseRedirect
        else:
            return http.HttpResponsePermanentRedirect

    def cms_redirect(self, redirect, query):
        """Returns the response object."""
        if not redirect.page and not redirect.new_path:
            return http.HttpResponseGone()

        response_class = self.get_cms_redirect_response_class(redirect)
        if redirect.page:
            if query:
                query = '?{query}'.format(query=query)
            redirect_to = '%s%s' % (redirect.page.get_absolute_url(), query)
        else:
            if query and '?' in redirect.new_path:
                query = '&{query}'.format(query=query)
            elif query:
                query = '?{query}'.format(query=query)

            redirect_to = '%s%s' % (redirect.new_path, query)

        return response_class(redirect_to)

    def process_exception(self, request, exception):
        """Handle 404 exceptions and check for redirects."""
        if not isinstance(exception, http.Http404):
            return

        parsed_path = urlparse(request.get_full_path())
        possible_paths = self.get_possible_paths(parsed_path)
        cms_redirect = self.get_cms_redirect(possible_paths)
        if cms_redirect:
            query = self.get_query(parsed_path)
            return self.cms_redirect(cms_redirect, query)
