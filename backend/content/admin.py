# content/admin.py

from django.contrib import admin
from .models import Project, PersonalInfo, Skill, SocialLink, Memory, MemoryPhoto

# This allows us to see and edit MemoryPhoto directly inside the Memory admin page.
class MemoryPhotoInline(admin.TabularInline):
    model = MemoryPhoto
    verbose_name = "Image URL"
    verbose_name_plural = "Image URLs"
    extra = 1  # Show 1 extra empty slot by default

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    inlines = [MemoryPhotoInline]
    list_display = ('title', 'date_of_memory')

# This customizes the admin page for the PersonalInfo model.
class PersonalInfoAdmin(admin.ModelAdmin):
    # The filter_horizontal makes selecting many skills/links easier.
    filter_horizontal = ('skills', 'social_links')

# --- NEW: Admin Configuration for Skills ---
# We create this class to better organize the Skill creation form.
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'image')
    # fieldsets organize the form into logical groups.
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Icon (Choose One)', {
            'description': "Use an image URL OR a Devicon class. The image URL will be used if both are filled.",
            'fields': ('image', 'icon_class'),
        }),
    )

# --- Final Registration of all models ---
# We now use our custom admin classes for a better experience.

admin.site.register(Project)
admin.site.register(PersonalInfo, PersonalInfoAdmin)
admin.site.register(Skill, SkillAdmin) # Use the new SkillAdmin
admin.site.register(SocialLink)
admin.site.register(Memory, MemoryAdmin)