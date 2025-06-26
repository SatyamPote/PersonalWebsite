from django.contrib import admin
from .models import Project, PersonalInfo, Skill, SocialLink, Memory

class PersonalInfoAdmin(admin.ModelAdmin):
    # This makes it easy to select skills, links, and memories
    filter_horizontal = ('skills', 'social_links', 'memories')

admin.site.register(Project)
admin.site.register(PersonalInfo, PersonalInfoAdmin)
admin.site.register(Skill)
admin.site.register(SocialLink)
admin.site.register(Memory)