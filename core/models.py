from django.db import models
from taggit.models import TagBase, GenericTaggedItemBase
from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField

# Create your models here.




class Profile(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile/')  # Geht direkt zu Cloudinary
    bio = models.TextField(blank=True)

    def __clstr__(self):
        return self.name
    
class PortfolioScreenshot(models.Model):
    """
    Screenshots für die 'About This Portfolio' Seite.
    Admin kann Screenshots hochladen und beschreiben.
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Titel",
        help_text="z.B. 'Guest Icon-Challenge Modal'"
    )
    
    image = models.ImageField(
        upload_to='portfolio/screenshots/',  # → Cloudinary
        verbose_name="Screenshot"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Beschreibung",
        help_text="Erkläre, was auf dem Screenshot zu sehen ist"
    )
    
    section = models.CharField(
        max_length=100,
        choices=[
            ('overview', '🎯 Projekt-Übersicht'),
            ('architecture', '🏗️ System-Architektur'),
            ('auth', '🔐 Auth-System'),
            ('deployment', '🚀 Deployment'),
            ('challenges', '💡 Technical Challenges'),
            ('apis', '🔌 API-Integrationen'),
        ],
        default='overview',
        verbose_name="Sektion"
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name="Reihenfolge",
        help_text="Niedrigere Zahlen = weiter oben"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['section', 'order', '-created_at']
        verbose_name = "Portfolio-Screenshot"
        verbose_name_plural = "Portfolio-Screenshots"
    
    def __str__(self):
        return f"{self.get_section_display()} - {self.title}"
    
    
    # ==========================================
# CURRENT PROJECT - TAGGIT MODELS
# ==========================================




class ColoredTag(TagBase):
    """Custom Tag Model mit Farbe für Tailwind"""
    
    COLOR_CHOICES = [
        ('purple', 'Purple'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('orange', 'Orange'),
        ('red', 'Red'),
        ('pink', 'Pink'),
        ('cyan', 'Cyan'),
        ('gray', 'Gray'),
    ]
    
    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default='gray',
        help_text='Tailwind color für diesen Tag'
    )
    
    class Meta:
        verbose_name = 'Tech Tag'
        verbose_name_plural = 'Tech Tags'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TaggedUpdate(GenericTaggedItemBase):
    """Through Model für Tag-Update Relation"""
    tag = models.ForeignKey(
        ColoredTag,
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )


class ProjectUpdate(models.Model):
    """Updates für Current Project"""
    
    UPDATE_TYPE_CHOICES = [
        ('milestone', '🎯 Milestone'),
        ('daily', '🔧 Daily Update'),
        ('feature', '✨ New Feature'),
        ('bugfix', '🐛 Bug Fix'),
        ('note', '📝 Note'),
    ]
    
    # ============ PFLICHTFELDER ============
    title = models.CharField(
        max_length=200,
        help_text='Kurze, prägnante Headline'
    )
    
    description = models.TextField(
        help_text='Vollständige Beschreibung (Markdown supported)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_current = models.BooleanField(
        default=True,
        help_text='Gehört zu aktuellem Projekt?'
    )
    
    # ============ KATEGORISIERUNG ============
    update_type = models.CharField(
        max_length=20,
        choices=UPDATE_TYPE_CHOICES,
        default='daily',
        help_text='Art des Updates'
    )
    
    tags = TaggableManager(
        through=TaggedUpdate,
        blank=True,
        help_text='Tags komma-getrennt eingeben (Auto-Complete!)'
    )
    
    # ============ OPTIONAL ============
    code_snippet = models.TextField(
        blank=True,
        help_text='Code-Snippet (optional)'
    )
    
    screenshot = CloudinaryField(
        'image',
        blank=True,
        null=True,
        folder='project_updates',
        help_text='Screenshot (optional)'
    )
    
    github_link = models.URLField(
        blank=True,
        help_text='Link zu GitHub Commit/PR (optional)'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project Update'
        verbose_name_plural = 'Project Updates'
    
    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d')} - {self.title}"
    
    def get_type_emoji(self):
        """Helper: Emoji basierend auf Type"""
        emojis = {
            'milestone': '🎯',
            'daily': '🔧',
            'feature': '✨',
            'bugfix': '🐛',
            'note': '📝',
        }
        return emojis.get(self.update_type, '📌')