from typing import Dict

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest

from dit_activity_stream.client import ActivityStreamClient


class TestActivityStreamClient(ActivityStreamClient):
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
