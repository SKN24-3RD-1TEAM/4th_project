from django.urls import path
from . import views

app_name="chats"

urlpatterns = [
    path('start/character/<int:charater_id>/', views.start_character_chat, name='start_character_chat'),
    path('start/story/<int:story_id>/', views.start_story_chat, name='start_story_chat'),
    path('<int:room_id>/', views.chat_room, name='room')
]