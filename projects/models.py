from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='projects/thumbnails/')
    # thumbnail = models.CharField(max_length=200, blank=True)  # Temporärer Ersatz
    technologies = models.CharField(max_length=300)
    github_url = models.URLField(blank=True)
    is_public_demo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class InvitedUser(models.Model): 
    email = models.EmailField(unique=True)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE) 
    invited_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    
    # Thumbnail → optional + darf leer sein
    thumbnail = models.ImageField(
        upload_to='projects/thumbnails/',
        blank=True,       # ← darf leer sein
        null=True,        # ← darf NULL in DB
        help_text="Optional – kannst du später hochladen"
    )
    
    technologies = models.CharField(max_length=300, verbose_name="Technologien")
    
    # Github-URL → kein URLField mehr → keine Prüfung!
    github_url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="z. B. https://github.com/... oder 'privat – auf Anfrage'"
    )
    
    # Optional: separates Feld für Live-Demo (falls du willst)
    live_demo_url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Nur bei öffentlichen Projekten, z. B. GitHub Pages Link"
    )
    
    is_public_demo = models.BooleanField(default=False, verbose_name="Öffentlich sichtbar?")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = "Projekt"
        verbose_name_plural = "Projekte"

    def __str__(self):
        return self.title


class InvitedUser(models.Model): 
    email = models.EmailField(unique=True)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    invited_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email