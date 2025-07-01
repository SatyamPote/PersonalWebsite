from django.contrib import admin
from .models import Project, PersonalInfo, Skill, SocialLink, Memory, MemoryPhoto

# This allows us to see and edit MemoryPhoto directly inside the Memory admin page.
class MemoryPhotoInline(admin.TabularInline):
    model = MemoryPhoto
    verbose_name = "Image URL"
    verbose_name_plural = "Image URLs"
    extra = 1

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    # This adds the photo URL fields to the Memory page.
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
        (None, {'fields': ('name',)}),
        ('Icon (Choose One)', {
            'description': "Use an image URL OR a Devicon class. The image URL will be used if both are filled.",
            'fields': ('image', 'icon_class'),
        }),
    )

# --- Final Registration of all  ---
# This ensures that all custom admin configurations are used.

admin.site.register(Project)
admin.site.register(PersonalInfo, PersonalInfoAdmin) # Uses the custom PersonalInfoAdmin
admin.site.register(Skill, SkillAdmin)
admin.site.register(SocialLink)
admin.site.register(Memory, MemoryAdmin)