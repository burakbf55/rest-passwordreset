from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import RequestDataTooBig
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

TOKEN_GENERATOR_CLASS = get_token_generator()


__all__ = [
    'RestPasswordToken',
    'get_password_reset_token_expiry_time',
    'get_password_reset_lookup_field',
    'clear_expired',
]


class ResetPasswordToken(models.Model):
    class Meta:
        verbose_name = ("Password Reset Token")
        verbose_name_plural = _("Password Reset Tokens")

    @staticmethod
    def generate_key():
        return TOKEN_GENERATOR_CLASS.generate_token()
    
    id = models.AutoField(
        primary_key=True
    )

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='password_reset_tokens',
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this password reset token")
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("When was this token generated")
    )

    key = models.CharField(
        _("Key"),
        max_length=64,
        db_index=True,
        unique=True
    )
    ip_address = models.GenericIPAddressField(
        _("The IP address of this session"),
        default="",
        blank=True,
        null=True
    )
    user_agent = models.CharField(
        max_length=256,
        verbose_name=_("HTTP User Agent"),
        default="",
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.key:# self key =! 1 ise demektir.
            self.key = self.generate_key()
        return super(ResetPasswordToken, self).save(*args, **kwargs)
    
    def __str__(self):
        return "Password reset token for user {user}".format(user = self.user)


def get_password_reset_token_expiry_time():
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME', 24)


def get_password_reset_lookup_field():

    return getattr(settings, 'DJANGO_REST_LOOKUP_FIELD', 'email')


def clear_expired(expiry_time):


    ResetPasswordToken.objects.filter(created_at__lte = expiry_time).delete()


def eligible_for_reset(self):
    if not self.is_active:
        return False
    
    if getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_REQUIRE_USABLE_PASSWORD', True):
        
        return self.has_usable_password()
    
    else:

        return True
    

UserModel = get_user_model()
UserModel.add_to_class("eligible_for_reset", eligible_for_reset)
