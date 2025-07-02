from django.shortcuts import render
from django.http import JsonResponse
from .models import PersonalInfo

# Your existing API view
def portfolio_data_api(request):
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
            'date_of_memory': memory.date_of_memory.strftime('%Y-%m-%d'),
            'photos': photos_urls
        })

    data = {
        "personal_info": personal_info_data,
        "social_links": social_links_data,
        "skills": skills_data,
        "projects": projects_data,
        "memories": memories_data,
    }

    return JsonResponse(data)

# This view renders your index.html
def index(request):
    # Ensure 'index.html' is in the 'templates/' directory at the project root.
    return render(request, 'index.html')
