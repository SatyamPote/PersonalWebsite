from django.db import models
from django.utils import timezone

# --- Define supporting models FIRST ---

class Skill(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.URLField(
        max_length=500,
        blank=True, 
        null=True,
        help_text="(Optional) Paste a direct image link for the skill icon (e.g., from Google Drive, Imgur)."
    )
    def __str__(self):
        return self.name

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

class MemoryPhoto(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='photos')
    image_url = models.URLField(max_length=500, help_text="Paste the direct image link here.")
    def __str__(self):
        return f"Photo for '{self.memory.title}'"

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project_url = models.URLField(blank=True, null=True, help_text="The main link for your project.")
    date_created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title

# --- Define the MAIN model LAST, as it references the others ---

class PersonalInfo(models.Model):
    full_name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    profile_photo_url = models.URLField(
        max_length=500,
        blank=True, 
        null=True,
        help_text="Paste a direct image link for your profile photo."
    )
    about_me = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    languages_spoken = models.CharField(max_length=200, blank=True)
    my_goals = models.TextField(blank=True)
    
    # These fields reference the models defined above
    skills = models.ManyToManyField(Skill, blank=True)
    social_links = models.ManyToManyField(SocialLink, blank=True)

    def __str__(self):
        return self.full_name