from typing import Dict

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import HttpRequest

from dit_activity_stream.client import ActivityStreamClient

User = get_user_model()


class TestBadActivityStreamClient:
    pass


class TestActivityStreamClient(ActivityStreamClient):
    object_uuid_field = "user_id"
    object_last_modified_field = "last_modified"

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return User.objects.all()

    def render_object(self, object: User) -> Dict:
        return {
            "Name": object.username,
        }


class CustomRenderClient(TestActivityStreamClient):
    def render_object(self, object):
        return {
            "username": object.username,
        }


class CustomQuerysetClient(TestActivityStreamClient):
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return User.objects.all().filter(username="Jack")
