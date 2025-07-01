from django.contrib import admin
from .models import Project, PersonalInfo, Skill, SocialLink, Memory, MemoryPhoto

# Registering PersonalInfo
@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    filter_horizontal = ('skills', 'social_links')  # M2M fields

# Inline for Memory photos
class MemoryPhotoInline(admin.TabularInline):
    model = MemoryPhoto
    verbose_name = "Image URL"
    verbose_name_plural = "Image URLs"
    extra = 1

# Memory admin with inline photos
@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    inlines = [MemoryPhotoInline]
    list_display = ('title', 'date_of_memory')

# Skill admin customization
@admin.register(Skill)
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

# Register remaining models
admin.site.register(Project)
admin.site.register(SocialLink)
