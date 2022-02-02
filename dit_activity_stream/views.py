import hmac

from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.module_loading import import_string
from django.views import View

from hawkserver import authenticate_hawk_header


# We want this function to return a View
def get_activity_stream_client():
    """
    Get the view from the DIT_ACTIVITY_STREAM_CLIENT_CLASS setting
    """

    # Use default view if RENDER_VIEW setting doesn't exist.
    if not getattr(settings, "DIT_ACTIVITY_STREAM_CLIENT_CLASS", None):
        return ActivityStreamClient()

    dit_activity_stream_client_class = import_string(settings.DIT_ACTIVITY_STREAM_CLIENT_CLASS)

    # Check if subclass of ActivityStreamClient
    if not issubclass(dit_activity_stream_client_class, ActivityStreamClient):
        raise ValueError("DIT_ACTIVITY_STREAM_CLIENT_CLASS must inherit from ActivityStreamClient")

    return dit_activity_stream_client_class()


class DitActivityStreamView(View):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.client = get_activity_stream_client()

    def dispatch(self, request, *args, **kwargs):
        if not self.authenticate(request):
            return self.forbidden()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.client.render_page(request)

    def authenticate(self, request):
        # Ensure not being accessed via public networking
        via_public_internet = "x-forwarded-for" in request.headers
        if via_public_internet:
            return False

        # Ensure signed with Hawk
        try:
            request.headers["authorization"]
        except KeyError:
            return False

        # This is brittle to not running in PaaS or not via private networking
        host, port = request.META["HTTP_HOST"].split(":")

        max_skew_seconds = 15
        error_message, credentials = authenticate_hawk_header(
            self.lookup_credentials,
            self.seen_nonce,
            max_skew_seconds,
            request.headers["authorization"],
            request.method,
            host,
            port,
            request.get_full_path(),
            request.headers.get("content-type", ""),
            request.body,
        )
        if error_message is not None:
            return False

        return True

    def forbidden(self):
        return JsonResponse(
            data={},
            status=403,
        )

    def lookup_credentials(self, passed_id):
        user = {
            "id": settings.ACTIVITY_STREAM_HAWK_CREDENTIALS["id"],
            "key": settings.ACTIVITY_STREAM_HAWK_CREDENTIALS["key"],
        }
        return user if hmac.compare_digest(passed_id, user["id"]) else None

    def seen_nonce(self, nonce, id):
        # No replay attack prevention since no shared cache between instances,
        # but we're ok with that for
        return False


class ActivityStreamClient:

    data_key = 'users'

    def get_queryset(self, request):
        return User.objects.all()

    def render_object(self, user):
        return {
            "Name": user.username,
        }

    def render_page(self, request):
        # Get the data
        data = {}
        users = self.get_queryset(request)
        
        data[self.data_key] = []
        for user in users:
            data[self.data_key].append(self.render_object(user))

        return JsonResponse(data)
