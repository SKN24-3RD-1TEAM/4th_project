from django.urls import path
from . import views

app_name = 'characters'

urlpatterns = [
    path('', views.character_list, name='list'),
    path('<int:character_id>/', views.character_detail, name='detail'),
]
