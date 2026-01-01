from django.contrib import admin
from .models import Profile, PortfolioScreenshot, ColoredTag, ProjectUpdate




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
    
    
    
# ==========================================
# CURRENT PROJECT ADMIN
# ==========================================

@admin.register(ColoredTag)
class ColoredTagAdmin(admin.ModelAdmin):
    """Admin für Tags mit Farben"""
    
    list_display = ['name', 'slug', 'color', 'color_badge', 'usage_count']
    list_editable = ['color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def color_badge(self, obj):
        """Zeigt Farbe als Badge"""
        colors = {
            'blue': '🔵', 'green': '🟢', 'purple': '🟣',
            'orange': '🟠', 'cyan': '🔷', 'yellow': '🟡',
            'pink': '🩷', 'red': '🔴', 'gray': '⚪',
        }
        return f"{colors.get(obj.color, '⚪')} {obj.color}"
    color_badge.short_description = 'Color'
    
    def usage_count(self, obj):
        """Anzahl verwendeter Updates"""
        return obj.tagged_items.count()
    usage_count.short_description = '# Uses'


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    """Admin für Project Updates mit Auto-Complete"""
    
    list_display = [
        'title',
        'update_type',
        'created_at',
        'has_screenshot',
        'has_code',
        'tag_list',
    ]
    
    list_filter = [
        'is_current',
        'update_type',
        'created_at',
        'tags',
    ]
    
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('📝 Pflichtfelder', {
            'fields': (
                'title',
                'description',
                'is_current',
            )
        }),
        ('🎯 Kategorisierung', {
            'fields': (
                'update_type',
                'tags',
            )
        }),
        ('⭐ Optional (kann leer bleiben)', {
            'classes': ('collapse',),
            'fields': (
                'code_snippet',
                'screenshot',
                'github_link',
            )
        }),
        ('🕐 Timestamps', {
            'classes': ('collapse',),
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def has_screenshot(self, obj):
        return '📸' if obj.screenshot else '—'
    has_screenshot.short_description = 'Screenshot'
    
    def has_code(self, obj):
        return '💻' if obj.code_snippet else '—'
    has_code.short_description = 'Code'
    
    def tag_list(self, obj):
        return ", ".join([t.name for t in obj.tags.all()])
    tag_list.short_description = 'Tags'