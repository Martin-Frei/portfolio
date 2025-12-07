# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_logs')
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-login_time']
        verbose_name = "Login-Log"
        verbose_name_plural = "Login-Logs"

    def __str__(self):
        return f"{self.user.email} – {self.login_time.strftime('%d.%m.%Y %H:%M')}"