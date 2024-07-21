from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FilmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "films"
    verbose_name = _("films")
