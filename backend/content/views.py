<<<<<<< HEAD
# content/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Project, PersonalInfo, Memory
=======
from django.http import JsonResponse
from .models import PersonalInfo
>>>>>>> parent of 0bbc509 (Refactor portfolio backend and frontend integration)

# Your existing API view
def portfolio_data_api(request):
<<<<<<< HEAD
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
        for skill in info.skills.all():
            skills_data.append({
                'name': skill.name,
                'icon_class': skill.icon_class,
                'image_url': skill.image if skill.image else None,
            })
        social_links_data = list(info.social_links.all().values('name', 'url'))
=======
    info = PersonalInfo.objects.prefetch_related(
        'skills', 
        'social_links', 
        'projects', 
        'memories__photos'
    ).first()

    if not info:
        return JsonResponse({'error': 'Portfolio data not configured in admin.'}, status=404)

    personal_info_data = {
        "full_name": info.full_name,
        "subtitle": info.subtitle,
        "profile_photo_url": info.profile_photo,
        "about_me": info.about_me,
        "location": info.location,
        "languages_spoken": info.languages_spoken,
        "my_goals": info.my_goals,
    }
>>>>>>> parent of 0bbc509 (Refactor portfolio backend and frontend integration)

    skills_data = [{
        'name': skill.name,
        'icon_class': skill.icon_class,
        'image_url': skill.image
    } for skill in info.skills.all()]

    social_links_data = list(info.social_links.all().values('name', 'url'))

    projects_data = [{
        'title': project.title,
        'description': project.description,
        'project_url': project.project_url
    } for project in info.projects.all().order_by('-date_created')]

    memories_data = []
    for memory in info.memories.all().order_by('-date_of_memory'):
        photos_urls = [photo.image_url for photo in memory.photos.all() if photo.image_url]
        memories_data.append({
            'title': memory.title,
            'description': memory.description,
            'link': memory.link,
<<<<<<< HEAD
            'date_of_memory': memory.date_of_memory,
            'photos': photos_urls,
        })

    return JsonResponse({
=======
            'date_of_memory': memory.date_of_memory.strftime('%Y-%m-%d'),
            'photos': photos_urls
        })
    
    data = {
>>>>>>> parent of 0bbc509 (Refactor portfolio backend and frontend integration)
        "personal_info": personal_info_data,
        "social_links": social_links_data,
        "skills": skills_data,
        "projects": projects_data,
        "memories": memories_data,
<<<<<<< HEAD
    }, safe=False)

# This view renders your index.html
def index(request):
    # Ensure 'index.html' is in the 'templates/' directory at the project root.
    return render(request, 'index.html')
=======
    }
    
    return JsonResponse(data)
>>>>>>> parent of 0bbc509 (Refactor portfolio backend and frontend integration)
