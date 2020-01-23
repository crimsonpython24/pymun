from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = _("Accounts")

    def ready(self):
        from . import signals
        from .models import User
        User = self.get_model('User')
