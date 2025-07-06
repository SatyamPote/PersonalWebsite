from django.db import models

class PersonalInfo(models.Model):
    full_name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    about_me = models.TextField()
    location = models.CharField(max_length=100)
    languages_spoken = models.CharField(max_length=200)
    my_goals = models.TextField()
    profile_photo_url = models.URLField(blank=True, null=True)  # ✅ Now using URLField

    def __str__(self):
        return self.full_name

class Skill(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # ✅ Replacing image upload with URLField

    def __str__(self):
        return self.name

class SocialLink(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, related_name='social_links', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class Project(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    project_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Memory(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, related_name='memories', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date_of_memory = models.DateField()

    def __str__(self):
        return self.title

class MemoryPhoto(models.Model):
    memory = models.ForeignKey(Memory, related_name='photos', on_delete=models.CASCADE)
    image_url = models.URLField()  # ✅ Now only using URLField for external images

    def __str__(self):
        return f"{self.memory.title} - Photo"
