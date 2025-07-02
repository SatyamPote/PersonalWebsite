<<<<<<< HEAD
# content/models.py
=======
>>>>>>> parent of 0bbc509 (Refactor portfolio backend and frontend integration)
from django.db import models
from django.utils import timezone

GOOGLE_PHOTOS_HELP_TEXT = """
For Google Photos: 1. Open the photo. 2. Click Share -> Create Link. 3. Open the new link in a new tab. 4. Right-click the image and select 'Copy Image Address'. Paste that link here. It should start with 'lh3.googleusercontent.com'.
"""

class Skill(models.Model):
    name = models.CharField(max_length=50)
<<<<<<< HEAD
    icon_class = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Optional. E.g., 'devicon-python-plain'"
    )
    image = models.URLField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Optional. Use if you don't have an icon class. Provide a direct image URL."
    )
=======
    icon_class = models.CharField(max_length=100, blank=True, null=True, help_text="Optional. Find class at devicon.dev. E.g., 'devicon-python-plain'")
    image = models.URLField(max_length=500, blank=True, null=True, help_text=f"Optional. Paste a direct image URL. {GOOGLE_PHOTOS_HELP_TEXT}")
>>>>>>> parent of 0bbc509 (Refactor portfolio backend and frontend integration)

    def __str__(self):
        return self.name

class MemoryPhoto(models.Model):
    memory = models.ForeignKey('Memory', on_delete=models.CASCADE, related_name='photos')
<<<<<<< HEAD
    image = models.URLField(
        max_length=500,
        help_text="Provide the direct URL to the photo."
    )
=======
    image_url = models.URLField("Direct Image URL", max_length=500, help_text=f"Paste the direct URL of the memory photo. {GOOGLE_PHOTOS_HELP_TEXT}")
>>>>>>> parent of 0bbc509 (Refactor portfolio backend and frontend integration)

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
    project_url = models.URLField(blank=True, null=True, help_text="The main link for your project (e.g., Live Demo or GitHub).")
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class PersonalInfo(models.Model):
    full_name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
<<<<<<< HEAD
    profile_photo = models.URLField(
        "Profile Photo URL",
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Provide the direct URL to your profile photo."
    )
=======
    profile_photo = models.URLField("Profile Photo URL", max_length=500, blank=True, null=True, help_text=f"Paste the direct URL to your profile photo. {GOOGLE_PHOTOS_HELP_TEXT}")
>>>>>>> parent of 0bbc509 (Refactor portfolio backend and frontend integration)
    about_me = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    languages_spoken = models.CharField(max_length=200, blank=True)
    my_goals = models.TextField(blank=True)
    
    skills = models.ManyToManyField(Skill, blank=True)
    social_links = models.ManyToManyField(SocialLink, blank=True)
    projects = models.ManyToManyField(Project, blank=True)
    memories = models.ManyToManyField(Memory, blank=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name_plural = "Personal Info"