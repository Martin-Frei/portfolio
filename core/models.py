from django.db import models

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