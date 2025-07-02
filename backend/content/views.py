# content/views.py
from django.http import JsonResponse
from .models import Project, PersonalInfo, Memory

def portfolio_data_api(request):
    # Get the single PersonalInfo object, if it exists
    info = PersonalInfo.objects.first()

    personal_info_data = {}
    skills_data = []
    social_links_data = []

    if info:
        personal_info_data = {
            "full_name": info.full_name,
            "subtitle": info.subtitle,
            "profile_photo_url": info.profile_photo if info.profile_photo else None,
            "about_me": info.about_me,
            "location": info.location,
            "languages_spoken": info.languages_spoken,
            "my_goals": info.my_goals,
        }

        # Get all skills associated with the PersonalInfo object
        for skill in info.skills.all():
            skills_data.append({
                'name': skill.name,
                'icon_class': skill.icon_class,
                'image_url': skill.image if skill.image else None,
            })

        # Get all social links associated with the PersonalInfo object
        social_links_data = list(info.social_links.all().values('name', 'url'))

    # Get all projects, ordered by most recent
    projects = Project.objects.all().order_by('-date_created')
    projects_data = list(projects.values('title', 'description', 'project_url'))

    # Get all memories, ordered by most recent
    memories_queryset = Memory.objects.all().order_by('-date_of_memory')
    memories_data = []
    for memory in memories_queryset:
        # Get all photo URLs for each memory
        photos_urls = [photo.image for photo in memory.photos.all()]
        memories_data.append({
            'title': memory.title,
            'description': memory.description,
            'link': memory.link,
            'date_of_memory': memory.date_of_memory,
            'photos': photos_urls,
        })

    # Combine all data into a single JSON response
    return JsonResponse({
        "personal_info": personal_info_data,
        "social_links": social_links_data,
        "skills": skills_data,
        "projects": projects_data,
        "memories": memories_data,
    }, safe=False)