from django.urls import path

from . import views

app_name = "images"

urlpatterns = [
    path("", views.image_page, name="image_page"),
    path("upload/", views.upload_image, name="upload_image"),
    path("delete/<int:pk>/", views.delete_image, name="delete_image"),
]
