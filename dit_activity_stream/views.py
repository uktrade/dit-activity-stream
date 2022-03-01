from django.conf import settings
from django.http import JsonResponse
from django.views import View

from dit_activity_stream.client import get_activity_stream_client


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

        # TODO: Use Django-Hawk to authenticate

        return True

    def forbidden(self):
        return JsonResponse(
            data={},
            status=403,
        )
