from django.contrib import admin
from .models import PersonalInfo, Skill, SocialLink, Project, Memory, MemoryPhoto

admin.site.register(PersonalInfo)
admin.site.register(Skill)
admin.site.register(SocialLink)
admin.site.register(Project)
admin.site.register(Memory)
admin.site.register(MemoryPhoto)
