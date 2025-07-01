# content/admin.py

from django.contrib import admin
from .models import Project, PersonalInfo, Skill, SocialLink, Memory, MemoryPhoto

class MemoryPhotoInline(admin.TabularInline):
    model = MemoryPhoto
    verbose_name = "Image URL"
    verbose_name_plural = "Image URLs"
    extra = 1 

class MemoryAdmin(admin.ModelAdmin):
    inlines = [MemoryPhotoInline]
    list_display = ('title', 'date_of_memory')

class PersonalInfoAdmin(admin.ModelAdmin):
    filter_horizontal = ('skills', 'social_links')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'image')
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Icon (Choose One)', {
            'description': "Use either a Devicon class name OR a direct image URL. The image URL will be used if both are provided.",
            'fields': ('icon_class', 'image'),
        }),
    )

admin.site.register(Project)
admin.site.register(PersonalInfo, PersonalInfoAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(SocialLink)
admin.site.register(Memory, MemoryAdmin)