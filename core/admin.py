from django.contrib import admin
from .models import Profile, PortfolioScreenshot 

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name',) 
    
    
@admin.register(PortfolioScreenshot)
class PortfolioScreenshotAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order', 'image_preview', 'created_at']
    list_filter = ['section', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['section', 'order', '-created_at']
    
    fieldsets = (
        ('Screenshot-Info', {
            'fields': ('title', 'image', 'description')
        }),
        ('Platzierung', {
            'fields': ('section', 'order'),
            'description': 'Lege fest, wo der Screenshot erscheinen soll.'
        }),
    )
    
    # Thumbnail in Admin anzeigen
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 200px;" />'
        return '-'
    image_preview.allow_tags = True
    image_preview.short_description = 'Vorschau'