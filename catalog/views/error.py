from django.shortcuts import render


def error_view(request, exception=None, status_code=500, message="Сталася помилка"):
    return render(
        request,
        "errors/base.html",
        {
            "status_code": status_code,
            "message": message,
        },
        status=status_code,
    )
