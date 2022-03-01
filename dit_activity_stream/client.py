from abc import ABC, abstractmethod
from typing import Any, Dict

from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse
from django.utils.module_loading import import_string


# We want this function to return a View
def get_activity_stream_client():
    """
    Get the view from the DIT_ACTIVITY_STREAM_CLIENT_CLASS setting
    """

    # Use default view if RENDER_VIEW setting doesn't exist.
    if not getattr(settings, "DIT_ACTIVITY_STREAM_CLIENT_CLASS", None):
        return ActivityStreamClient()

    dit_activity_stream_client_class = import_string(
        settings.DIT_ACTIVITY_STREAM_CLIENT_CLASS
    )

    # Check if subclass of ActivityStreamClient
    if not issubclass(dit_activity_stream_client_class, ActivityStreamClient):
        raise ValueError(
            "DIT_ACTIVITY_STREAM_CLIENT_CLASS must inherit from ActivityStreamClient"
        )

    return dit_activity_stream_client_class()


class ActivityStreamClient(ABC):
    @abstractmethod
    def get_data_key(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        raise NotImplementedError()

    @abstractmethod
    def render_object(self, object: Any) -> Dict:
        raise NotImplementedError()

    def render_page(self, request: HttpRequest) -> JsonResponse:
        objects = self.get_queryset(request)

        object_data = []
        for object in objects:
            object_data[self.get_data_key()].append(
                self.render_object(object=object),
            )

        return JsonResponse(
            {
                self.data_key: object_data,
            }
        )