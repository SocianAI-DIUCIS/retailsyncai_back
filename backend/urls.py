from django.urls import path, include
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok", "api": "/api/"})

urlpatterns = [
    path("", health, name="health"),
    path("api/", include("api.urls")),
]

