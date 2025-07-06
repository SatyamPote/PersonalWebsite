from django.http import JsonResponse
from content.models import PersonalInfo

def user_data(request):
    info = PersonalInfo.objects.prefetch_related(
        'skills', 'social_links', 'projects', 'memories__photos'
    ).first()

    if not info:
        return JsonResponse({"error": "No data found"}, status=404)

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
                "image_url": request.build_absolute_uri(skill.image.url) if skill.image else ""
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

from django.http import HttpResponse

def index(request):
    return HttpResponse("Backend is running ✅")
