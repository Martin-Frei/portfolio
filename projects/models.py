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
    
    