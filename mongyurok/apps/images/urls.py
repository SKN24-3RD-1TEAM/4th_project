from django.urls import path

from .views import ImageListView

app_name = "images"

urlpatterns = [
    path("", ImageListView.as_view(), name="list"),
]
