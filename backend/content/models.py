from django.db import models
from django.utils import timezone

class Skill(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.URLField(max_length=500, blank=True, help_text="Paste a direct link to a skill icon image.")
    def __str__(self): return self.name

class SocialLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    def __str__(self): return self.name

class Memory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    # Now just ONE simple URL field for the memory's image
    image_url = models.URLField(max_length=500, blank=True)
    date_of_memory = models.DateField(default=timezone.now)
    def __str__(self): return self.title

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project_url = models.URLField(blank=True, null=True)
    def __str__(self): return self.title

class PersonalInfo(models.Model):
    full_name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    # The profile photo is now just a URL
    profile_photo_url = models.URLField(max_length=500, blank=True)
    about_me = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    languages_spoken = models.CharField(max_length=200, blank=True)
    my_goals = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    social_links = models.ManyToManyField(SocialLink, blank=True)
    # We will link memories directly here for simplicity
    memories = models.ManyToManyField(Memory, blank=True)
    def __str__(self): return self.full_name