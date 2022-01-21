from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.module_loading import import_string
from django.views import View


# We want this function to return a View
def get_activity_stream_client():
    """
    Get the view from the DIT_ACTIVITY_STREAM_CLIENT_CLASS setting
    """

    # Use default view if RENDER_VIEW setting doesn't exist.
    if not getattr(settings, "DIT_ACTIVITY_STREAM_CLIENT_CLASS", None):
        return ActivityStreamClient()

    dit_activity_stream_client_class = import_string(settings.DIT_ACTIVITY_STREAM_CLIENT_CLASS)

    # Check if subclass of View
    if not issubclass(dit_activity_stream_client_class, ActivityStreamClient):
        raise ValueError("DIT_ACTIVITY_STREAM_CLIENT_CLASS must inherit from ActivityStreamClient")

    return dit_activity_stream_client_class()


class DitActivityStreamView(View):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.client = get_activity_stream_client()

    def get(self, request, *args, **kwargs):
        data = {}
        users = self.client.get_queryset()
        data["users"] = []
        for user in users:
            data["users"].append(self.client.render_object(user))
        return JsonResponse(data)


class ActivityStreamClient:

    def get_queryset(self):
        return User.objects.all()

    def render_object(self, user):
        return {
            "Name": user.username,
        }
