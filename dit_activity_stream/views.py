from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.module_loading import import_string
from django.views import View


# We want this function to return a View
def get_activity_stream_view() -> View:
    """
    Get the view from the RENDER_VIEW setting
    """

    # Use default view if RENDER_VIEW setting doesn't exist.
    if not getattr(settings, "RENDER_VIEW", None):
        return DitActivityStreamView.as_view()

    render_view_class = import_string(settings.RENDER_VIEW)

    # Check if subclass of View
    if not issubclass(render_view_class, View):
        raise ValueError("RENDER_VIEW must inherit from View")

    return render_view_class.as_view()


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
