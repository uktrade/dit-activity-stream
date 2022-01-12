from django.http import JsonResponse
from django.contrib.auth.models import User


def get_queryset():
    return User.objects.all()


def render_user(user):
    return {
            "Name": user.username,
        }


def index(request):
    data = {}
    users = get_queryset()
    data["users"] = []
    for user in users:
        data["users"].append(render_user(user))
    return JsonResponse(data)