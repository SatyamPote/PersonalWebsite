from rest_framework.views import APIView
from rest_framework.response import Response

class DashboardDataView(APIView):
    def get(self, request):
        data = {
            "todo_count": 5,
            "notes_count": 12,
            "weather": {
                "location": "New York",
                "temp": 28,
                "condition": "Sunny"
            },
            "github": {
                "repos": 10,
                "stars": 45
            }
        }
        return Response(data)
