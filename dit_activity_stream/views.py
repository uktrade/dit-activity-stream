from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View


def get_activity_stream_view():
    return DitActivityStreamView.as_view()


class DitActivityStreamView(View):

    def get(self, request, *args, **kwargs):
        data = {}
        users = self.get_queryset()
        data["users"] = []
        for user in users:
            data["users"].append(self.render_object(user))
        return JsonResponse(data)

    def get_queryset(self):
        return User.objects.all()

    def render_object(self, user):
        return {
            "Name": user.username,
        }
