from django.db import models
from django.utils import timezone

# --- DEFINED FIRST, since PersonalInfo needs it ---
class Skill(models.Model):
    name = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='skill_icons/', blank=True, null=True, help_text="Upload custom skill icon.")

    def __str__(self):
        return self.name

# --- MOVED UP, since PersonalInfo needs it ---
class SocialLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.name

class Memory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    date_of_memory = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

# --- DEFINED AFTER Memory, since it needs it ---
class MemoryPhoto(models.Model):
    memory = models.ForeignKey('Memory', on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='memories/')

    def __str__(self):
        return f"Photo for '{self.memory.title}'"

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project_url = models.URLField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

# --- NOW PersonalInfo can be defined because Skill and SocialLink exist ---
class PersonalInfo(models.Model):
    full_name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    about_me = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    languages_spoken = models.CharField(max_length=200, blank=True)
    my_goals = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    social_links = models.ManyToManyField(SocialLink, blank=True) # This will now work correctly

    def __str__(self):
        return self.full_name