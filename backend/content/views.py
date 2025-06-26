from django.http import JsonResponse
from .models import Project, PersonalInfo, Memory, Skill, SocialLink

def portfolio_data_api(request):
    info = PersonalInfo.objects.first()
    if not info:
        return JsonResponse({}) # Return empty if no profile is set up

    skills_data = list(info.skills.all().values('name', 'image_url'))
    social_links_data = list(info.social_links.all().values('name', 'url'))
    projects_data = list(Project.objects.all().order_by('-date_created').values('title', 'description', 'project_url'))
    memories_data = list(info.memories.all().order_by('-date_of_memory').values('title', 'description', 'image_url', 'date_of_memory'))
    
    personal_info_data = {
        "full_name": info.full_name,
        "subtitle": info.subtitle,
        "profile_photo_url": info.profile_photo_url,
        "about_me": info.about_me,
        "location": info.location,
        "languages_spoken": info.languages_spoken,
        "my_goals": info.my_goals,
    }

    data = {
        "personal_info": personal_info_data,
        "social_links": social_links_data,
        "skills": skills_data,
        "projects": projects_data,
        "memories": memories_data,
    }
    return JsonResponse(data)