import mimetypes

from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse

FRONTEND_ROOT = (settings.BASE_DIR / "coderr_frontend").resolve()


def frontend_file(request, path="index.html"):
    requested_file = (FRONTEND_ROOT / path).resolve()
    try:
        requested_file.relative_to(FRONTEND_ROOT)
    except ValueError as error:
        raise Http404 from error

    if not requested_file.is_file():
        raise Http404

    content_type, _ = mimetypes.guess_type(str(requested_file))
    return FileResponse(
        requested_file.open("rb"),
        content_type=content_type or "application/octet-stream",
    )


def health_check(request):
    return JsonResponse(
        {
            "name": "Coderr API",
            "status": "online",
            "api": "/api/",
        }
    )
