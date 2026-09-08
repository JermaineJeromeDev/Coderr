from django.http import JsonResponse


def health_check(request):
    return JsonResponse(
        {
            "name": "Coderr API",
            "status": "online",
            "api": "/api/",
        }
    )
