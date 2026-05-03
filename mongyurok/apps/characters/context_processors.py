from apps.characters.models import CharRoomSettings
from apps.scenarios.models import SceneRoomSetting

def sidebar_rooms(request):
    if not request.user.is_authenticated:
        return {}

    return {
        'char_rooms':  CharRoomSettings.objects.filter(user=request.user).order_by('-created_at')[:10],
        'scene_rooms': SceneRoomSetting.objects.filter(user=request.user).order_by('-created_at')[:10],
    }