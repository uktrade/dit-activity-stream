# DIT Activity Stream


## How to implement?

Example Client for returning all users:
```python
from typing import Any, Dict

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest

from dit_acivity_stream.client import ActivityStreamClient


class ActivityStreamUserClient(ActivityStreamClient):
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return User.objects.all()

    def render_object(self, object: User) -> Dict:
        return {
            "id": object.id,
            "username": object.username,
            "first_name": object.first_name,
            "last_name": object.last_name,
        }
```

Set `DIT_ACTIVITY_STREAM_CLIENT_CLASS` in your django settings file:

```python
DIT_ACTIVITY_STREAM_CLIENT_CLASS = "package.client.ActivityStreamUserClient"
```
