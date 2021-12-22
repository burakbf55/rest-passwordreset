from django.contrib import admin
from django_rest_passwordreset.models import ResetPasswordToken

# Register your models here.


@admin.site.register(ResetPasswordToken)
class RestPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key' ,'created_at', 'ip_address', 'user_agent')
    