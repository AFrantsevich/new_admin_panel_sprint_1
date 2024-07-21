from django.conf import settings
from movies_backend.settings.components.common import INSTALLED_APPS

LOCALE_PATHS = ["films/locale"]
LANGUAGE_CODE = "ru-RU"

INSTALLED_APPS += [
    "films.apps.FilmsConfig",
]

if settings.DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
