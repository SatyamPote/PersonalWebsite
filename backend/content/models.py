from django.db import models
from django.utils import timezone

class Skill(models.Model):
    name = models.CharField(max_length=50)
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="(Optional) Find the class name at devicon.dev. Example: 'devicon-python-plain'"
    )
    # --- CHANGED FROM ImageField to URLField ---
    image = models.URLField(max_length=500, blank=True, null=True, help_text="(Optional) Use a direct image URL.")

    def __str__(self):
        return self.name

class MemoryPhoto(models.Model):
    memory = models.ForeignKey('Memory', on_delete=models.CASCADE, related_name='photos')
    # --- CHANGED FROM ImageField to URLField ---
    image = models.URLField(max_length=500, help_text="Provide the direct URL to the image.")

    def __str__(self):
        return f"Photo for '{self.memory.title}'"

class Memory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    date_of_memory = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

class SocialLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project_url = models.URLField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class PersonalInfo(models.Model):
    full_name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    # --- CHANGED FROM ImageField to URLField ---
    profile_photo = models.URLField(max_length=500, blank=True, null=True)
    about_me = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    languages_spoken = models.CharField(max_length=200, blank=True)
    my_goals = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    social_links = models.ManyToManyField(SocialLink, blank=True)

    def __str__(self):
        return self.full_name