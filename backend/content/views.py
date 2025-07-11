# portfolio_api/views.py

from django.http import JsonResponse, HttpResponse
from .models import PersonalInfo

def index(request):
    return HttpResponse("Welcome to the Portfolio API!")

def user_data(request):
    try:
        info = PersonalInfo.objects.prefetch_related(
            'skills', 'social_links', 'projects', 'memories__photos'
        ).first()

        if not info:
            return JsonResponse({"error": "No personal info found"}, status=404)

        data = {
            "personal_info": {
                "full_name": info.full_name,
                "subtitle": info.subtitle,
                "about_me": info.about_me,
                "location": info.location,
                "languages_spoken": info.languages_spoken,
                "my_goals": info.my_goals,
                "profile_photo_url": info.profile_photo_url or "",
            },
            "social_links": [
                {"name": link.name, "url": link.url}
                for link in info.social_links.all()
            ],
            "skills": [
                {
                    "name": skill.name,
                    "icon_class": skill.icon_class,
                    "image_url": skill.image or ""
                }
                for skill in info.skills.all()
            ],
            "projects": [
                {
                    "title": project.title,
                    "description": project.description,
                    "project_url": project.project_url
                }
                for project in info.projects.all()
            ],
            "memories": [
                {
                    "title": memory.title,
                    "date_of_memory": memory.date_of_memory.isoformat(),
                    "photos": [photo.image_url for photo in memory.photos.all()]
                }
                for memory in info.memories.all()
            ]
        }

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
