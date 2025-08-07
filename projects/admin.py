from django.contrib import admin
from .models import Project, InvitedUser

# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'technologies', 'created_date']
    list_filter = ['created_date', 'technologies']
    search_fields = ['title', 'description']
    ordering = ['-created_date']


@admin.register(InvitedUser)
class InvitedUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'invited_by', 'invited_date']
    list_filter = ['invited_date']
    search_fields = ['email']
    ordering = ['-invited_date']