from django.http import JsonResponse
from .models import Project, PersonalInfo, Memory, Skill, SocialLink

def portfolio_data_api(request):
    info = PersonalInfo.objects.first()
    
    personal_info_data = {}
    skills_data = []
    social_links_data = []

    if info:
        personal_info_data = {
            "full_name": info.full_name,
            "subtitle": info.subtitle,
            "profile_photo_url": info.profile_photo.url if info.profile_photo else None,
            "about_me": info.about_me,
            "location": info.location,
            "languages_spoken": info.languages_spoken,
            "my_goals": info.my_goals,
        }
        
        # UPDATED: Get all skill data, including the new image URL
        for skill in info.skills.all():
            skills_data.append({
                'name': skill.name,
                'icon_class': skill.icon_class,
                'image_url': skill.image.url if skill.image else None
            })

        social_links_data = list(info.social_links.all().values('name', 'url'))

    projects = Project.objects.all().order_by('-date_created')
    projects_data = list(projects.values('title', 'description', 'project_url'))

    memories_queryset = Memory.objects.all().order_by('-date_of_memory')
    memories_data = []
    for memory in memories_queryset:
        photos_urls = [photo.image.url for photo in memory.photos.all()]
        memories_data.append({
            'title': memory.title,
            'description': memory.description,
            'link': memory.link,
            'date_of_memory': memory.date_of_memory,
            'photos': photos_urls
        })

    data = {
        "personal_info": personal_info_data,
        "social_links": social_links_data,
        "skills": skills_data,
        "projects": projects_data,
        "memories": memories_data,
    }
    
    return JsonResponse(data, safe=False)