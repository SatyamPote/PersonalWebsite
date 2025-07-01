# content/admin.py

from django.contrib import admin
from .models import Project, PersonalInfo, Skill, SocialLink, Memory, MemoryPhoto

# This tells Django how to display the photo URL fields inline for a Memory.
class MemoryPhotoInline(admin.TabularInline):
    model = MemoryPhoto
    verbose_name = "Image URL"
    verbose_name_plural = "Image URLs"
    extra = 1

# This customizes the admin page for the Memory model itself.
class MemoryAdmin(admin.ModelAdmin):
    inlines = [MemoryPhotoInline]
    list_display = ('title', 'date_of_memory')

# --- ★ THIS IS THE UPDATED SECTION ★ ---
# This customizes the admin page for the PersonalInfo model.
# We are adding a list_display to make it cleaner.
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subtitle') # Makes the main list view look nicer.
    
    # This line is correct and creates the two-box selection widget.
    # It allows you to link existing Skills and Social Links.
    filter_horizontal = ('skills', 'social_links')

# This customizes the admin page for the Skill model.
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

# --- Final Registration of all  ---
# This ensures that all custom admin configurations are used.

admin.site.register(Project)
admin.site.register(PersonalInfo, PersonalInfoAdmin) # Uses the custom PersonalInfoAdmin
admin.site.register(Skill, SkillAdmin)
admin.site.register(SocialLink)
admin.site.register(Memory, MemoryAdmin)