from django.http import JsonResponse
from .models import PersonalInfo  # We only need to query PersonalInfo

def portfolio_data_api(request):
    """
    This single, robust view fetches the main PersonalInfo object and follows
    its relationships to build the exact JSON structure the frontend needs.
    """
    # 1. Get the single PersonalInfo object. This is the "root" of all your data.
    info = PersonalInfo.objects.prefetch_related(
        'skills', 
        'social_links', 
        'projects', 
        'memories__photos'  # Deeply fetch memories AND their related photos in one go
    ).first()

    # If no PersonalInfo has been created in the admin, return an error.
    if not info:
        return JsonResponse({'error': 'Portfolio data has not been configured in the admin panel.'}, status=404)

    # 2. Serialize the main info.
    #    The 'if info.profile_photo else None' pattern safely handles empty image fields.
    personal_info_data = {
        "full_name": info.full_name,
        "subtitle": info.subtitle,
        "profile_photo_url": info.profile_photo if info.profile_photo else None,
        "about_me": info.about_me,
        "location": info.location,
        "languages_spoken": info.languages_spoken,
        "my_goals": info.my_goals,
    }

    # 3. Serialize ONLY the skills linked to this PersonalInfo object.
    skills_data = [
        {
            'name': skill.name,
            'icon_class': skill.icon_class,
            'image_url': skill.image if skill.image else None
        } 
        for skill in info.skills.all()
    ]

    # 4. Serialize ONLY the social links linked to this PersonalInfo object.
    social_links_data = list(info.social_links.all().values('name', 'url'))

    # 5. Serialize ONLY the projects linked to this PersonalInfo object.
    projects_data = [
        {
            'title': project.title,
            'description': project.description,
            'project_url': project.project_url
        }
        for project in info.projects.all().order_by('-date_created')
    ]

    # 6. Serialize ONLY the memories linked to this PersonalInfo object.
    memories_data = []
    for memory in info.memories.all().order_by('-date_of_memory'):
        # For each memory, get the URLs of its related photos.
        photos_urls = [photo.image_url for photo in memory.photos.all() if photo.image_url]
        
        memories_data.append({
            'title': memory.title,
            'description': memory.description,
            'link': memory.link,
            'date_of_memory': memory.date_of_memory.strftime('%Y-%m-%d'),
            'photos': photos_urls
        })
    
    # 7. Assemble the final data structure, just like your frontend expects.
    data = {
        "personal_info": personal_info_data,
        "social_links": social_links_data,
        "skills": skills_data,
        "projects": projects_data,
        "memories": memories_data,
    }
    
    return JsonResponse(data)