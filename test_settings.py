"""Django settings file for testing."""
import os

HELPER_SETTINGS = dict(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },

    INSTALLED_APPS=(
        # 'django.contrib.sites',
        # 'django.contrib.messages',
        # 'django.contrib.auth',
        # 'django.contrib.contenttypes',
        # 'cms',
        # 'mptt',
        # 'menus',
        # 'sekizai',
        'cms_redirects',
    ),

    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.doc.XViewMiddleware',
        'django.middleware.common.CommonMiddleware',
        'cms.middleware.user.CurrentUserMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware',
        'cms.middleware.language.LanguageCookieMiddleware',
        'cms_redirects.middleware.RedirectMiddleware',
    ),

    TEMPLATE_CONTEXT_PROCESSORS=(
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.i18n',
        'django.core.context_processors.request',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'sekizai.context_processors.sekizai',
        'cms.context_processors.cms_settings',
    ),

    TEMPLATE_DIRS=(
        # Put strings here like "/home/html/django_templates" or
        # "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        os.path.join(os.path.dirname(__file__), 'cms_redirects', 'tests', 'templates'),
    ),

    CMS_TEMPLATES=(
        ('template_1.html', 'Template One'),
    ),

    LANGUAGES=[
        ('en', 'English'),
    ],
    LANGUAGE_CODE='en',

    SITE_ID=1,
    SECRET_KEY='abcde12345',
    ROOT_URLCONF='test_urls',

    STATIC_URL='/static/',

    TEST_RUNNER='django_nose.NoseTestSuiteRunner',

    MIGRATION_MODULES={
        'cms': 'cms.migrations_django',
        'menus': 'menus.migrations_django',

        # Add also the following modules if you're using these plugins:
        'djangocms_file': 'djangocms_file.migrations_django',
        'djangocms_flash': 'djangocms_flash.migrations_django',
        'djangocms_googlemap': 'djangocms_googlemap.migrations_django',
        'djangocms_inherit': 'djangocms_inherit.migrations_django',
        'djangocms_link': 'djangocms_link.migrations_django',
        'djangocms_picture': 'djangocms_picture.migrations_django',
        'djangocms_snippet': 'djangocms_snippet.migrations_django',
        'djangocms_teaser': 'djangocms_teaser.migrations_django',
        'djangocms_video': 'djangocms_video.migrations_django',
        'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
    }
)

