from django.db import models
from django.conf import settings
from apps.users.models import User

class SceneModeInfo(models.Model):
    """
    역할극 모드 전체 목록 및 시나리오 설정 정보
    """
    title = models.CharField(max_length=200, verbose_name="시나리오 제목")
    summary = models.TextField(verbose_name="시나리오 개요")
    
    keyword1 = models.CharField(max_length=50, blank=True, null=True, verbose_name="키워드 1")
    keyword2 = models.CharField(max_length=50, blank=True, null=True, verbose_name="키워드 2")
    keyword3 = models.CharField(max_length=50, blank=True, null=True, verbose_name="키워드 3")
    
    default_personality = models.TextField(verbose_name="기본 성격")
    default_identity = models.TextField(verbose_name="기본 정체성")
    default_values = models.TextField(verbose_name="기본 가치관")
    default_first_scene = models.TextField(verbose_name="첫 장면 상황 설명")

    class Meta:
        db_table = 'scene_mode_info'
        verbose_name = '역할극 시나리오 정보'
        verbose_name_plural = '역할극 시나리오 정보 목록'
        ordering = ['title']

    def __str__(self):
        return self.title


class SceneCharInfo(models.Model):
    """
    스토리에 등장하는 캐릭터 정보 (메인 캐릭터 및 엑스트라)
    """
    scene = models.ForeignKey(SceneModeInfo, on_delete=models.CASCADE, related_name='chars', verbose_name="소속 스토리")
    name = models.CharField(max_length=100, verbose_name="캐릭터 이름")
    keyword = models.CharField(max_length=200, blank=True, null=True, verbose_name="캐릭터 키워드(성격 등)")
    summary = models.TextField(blank=True, null=True, verbose_name="캐릭터 한 줄 요약 및 설명")
    is_extra = models.BooleanField(default=False, blank=True, verbose_name="캐릭터 역할")
    img_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="프로필 이미지 URL")

    class Meta:
        db_table = 'scene_char_info'
        verbose_name = '역할극 캐릭터 정보'
        verbose_name_plural = '역할극 캐릭터 정보 목록'

    def __str__(self):
        role = "엑스트라" if self.is_extra else "메인 캐릭터"
        return f"[{role}] {self.name} ({self.scene_id.title})"


class SceneRoomSetting(models.Model):
    """
    사용자가 생성한 역할극 채팅방 정보 및 설정
    """
    class MessageLength(models.TextChoices):
        SHORT = 'short'
        NORMAL = 'normal'
        LONG = 'long'
        VERY_LONG = 'very_long'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scene_rooms", verbose_name="사용자 ID")
    scene = models.ForeignKey(SceneModeInfo, on_delete=models.CASCADE, related_name="rooms", verbose_name="시나리오 ID")
    persona = models.OneToOneField('characters.Persona', on_delete=models.SET_NULL, null=True, blank=True, related_name="scene_room", verbose_name="적용된 페르소나 ID")
    
    msg_len = models.CharField(max_length=20, choices=MessageLength.choices, default=MessageLength.NORMAL, verbose_name="답변 길이 설정")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")

    class Meta:
        db_table = 'scene_room_settings'
        verbose_name = '역할극 채팅방 설정'
        verbose_name_plural = '역할극 채팅방 설정 목록'

    def __str__(self):
        return f"{self.user}'s room for {self.scene.title}"


class SceneMessage(models.Model):
    """
    채팅방 내에서 오고 간 메시지 내역
    """
    class MessageType(models.TextChoices):
        SCENE = 'scene'
        USER = 'user'
        CHARACTER = 'character'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scene_messages', verbose_name="사용자 ID")
    room = models.ForeignKey(SceneRoomSetting, on_delete=models.CASCADE, related_name='messages', verbose_name="채팅방 ID")
    char = models.ForeignKey(SceneCharInfo, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages', verbose_name="발화 캐릭터")
    
    type = models.CharField(max_length=20, choices=MessageType.choices, verbose_name="메시지 타입")
    content = models.TextField(verbose_name="메시지 내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")

    class Meta:
        db_table = 'scene_messages'
        verbose_name = '역할극 채팅 메시지'
        verbose_name_plural = '역할극 채팅 메시지 목록'
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.get_type_display()}] {self.content[:20]}..."