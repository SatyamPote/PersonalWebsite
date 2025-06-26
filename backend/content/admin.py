from django.contrib import admin
from .models import Project, PersonalInfo, Skill, SocialLink, Memory, MemoryPhoto

# --- New Admin Configurations for Memories ---

# This tells Django how to display the photo upload fields. 'TabularInline' is compact.
class MemoryPhotoInline(admin.TabularInline):
    model = MemoryPhoto
    extra = 1  # Show 1 extra empty upload slot by default

# This customizes the admin page for the Memory model itself.
class MemoryAdmin(admin.ModelAdmin):
    # This is the magic line that adds the photo uploader to the Memory page.
    inlines = [MemoryPhotoInline]

# --- Admin Configuration for PersonalInfo (from before) ---

class PersonalInfoAdmin(admin.ModelAdmin):
    filter_horizontal = ('skills', 'social_links')


# --- Final Registration of all models ---

admin.site.register(Project)
admin.site.register(PersonalInfo, PersonalInfoAdmin)
admin.site.register(Skill)
admin.site.register(SocialLink)
admin.site.register(Memory, MemoryAdmin) # Use the new MemoryAdmin class
# We don't need to register MemoryPhoto separately because it's handled by the inline.