# accounts/admin.py
from django.contrib import admin
from .models import LoginLog

@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'login_time', 'ip_address']
    list_filter = ['login_time']
    search_fields = ['user__email']
    readonly_fields = ['user', 'login_time', 'ip_address', 'user_agent']
    date_hierarchy = 'login_time'