from django.http import JsonResponse
from .models import Project, PersonalInfo, Memory, Skill, SocialLink

def portfolio_data_api(request):
    # This is the main object we need. It might not exist yet.
    info = PersonalInfo.objects.first()
    
    # --- Prepare empty data structures ---
    personal_info_data = {}
    skills_data = []
    social_links_data = []
    memories_data = []
    # Fetch all projects regardless of whether a profile exists
    projects_data = list(Project.objects.all().order_by('-date_created').values('title', 'description', 'project_url'))

    # --- THE FIX: Only try to get related data IF the 'info' object exists ---
    if info:
        # If a PersonalInfo object exists, populate its data
        personal_info_data = {
            "full_name": info.full_name,
            "subtitle": info.subtitle,
            "profile_photo_url": info.profile_photo_url,
            "about_me": info.about_me,
            "location": info.location,
            "languages_spoken": info.languages_spoken,
            "my_goals": info.my_goals,
        }
        
        # Also get the data related to this specific profile
        skills_data = list(info.skills.all().values('name', 'image_url'))
        social_links_data = list(info.social_links.all().values('name', 'url'))
        memories_data = list(info.memories.all().order_by('-date_of_memory').values('title', 'description', 'image_url', 'date_of_memory'))
    
    # --- Assemble the final data payload ---
    # This will now work even if some parts are empty.
    data = {
        "personal_info": personal_info_data,
        "social_links": social_links_data,
        "skills": skills_data,
        "projects": projects_data,
        "memories": memories_data,
    }
    
    # Use JsonResponse's built-in encoder, which is safer
    return JsonResponse(data)