from django.contrib import admin
from .models import Project, PersonalInfo, Skill, SocialLink, Memory, MemoryPhoto

# This allows us to see and edit MemoryPhoto directly inside the Memory admin page.
class MemoryPhotoInline(admin.TabularInline):
    model = MemoryPhoto
    verbose_name = "Image URL"
    verbose_name_plural = "Image URLs"
    extra = 1  # Show 1 extra empty slot

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    inlines = [MemoryPhotoInline]
    list_display = ('title', 'date_of_memory')
    search_fields = ('title',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'image')
    search_fields = ('name',)
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Icon (Choose One)', {
            'description': "Use an image URL OR a Devicon class. The image URL will be used if both are filled.",
            'fields': ('image', 'icon_class'),
        }),
    )

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'icon_class')
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_url', 'date_created')
    search_fields = ('title',)

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    # filter_horizontal is much better for ManyToMany fields
    filter_horizontal = ('skills', 'social_links', 'projects', 'memories')
    
    def __str__(self):
        return "Main Portfolio Configuration"
        
# We don't need a separate admin for MemoryPhoto since it's an inline
# admin.site.register(MemoryPhoto)