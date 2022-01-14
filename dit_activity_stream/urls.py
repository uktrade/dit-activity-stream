from django.urls import path

from dit_activity_stream import views

urlpatterns = [
    path('', views.get_activity_stream_view()),
]
