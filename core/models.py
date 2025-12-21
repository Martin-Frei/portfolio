from django.db import models

# Create your models here.




class Profile(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile/')  # Geht direkt zu Cloudinary
    bio = models.TextField(blank=True)

    def __clstr__(self):
        return self.name