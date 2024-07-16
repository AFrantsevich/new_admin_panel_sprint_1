from movies_backend.settings.components.common import INSTALLED_APPS

LOCALE_PATHS = ["films/locale"]
LANGUAGE_CODE = "ru-RU"

INSTALLED_APPS += ["films.apps.FilmsConfig"]
