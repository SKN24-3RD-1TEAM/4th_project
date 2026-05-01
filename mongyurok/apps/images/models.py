"""이미지 도메인 모델.

요구사항서 기준:
- img        : 생성된 이미지 자체
- img_used   : 이미지가 사용된 이력 (어떤 채팅/스토리에서 사용했는지)

이미지 페이지(REQ-HIST-04)에서는 `Img` 중 ImgUsed가 1건 이상 존재하는
레코드만 최신순으로 보여준다.
"""
from django.conf import settings
from django.db import models


class Img(models.Model):
    """생성된 이미지 1건.

    DB table: img
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
        verbose_name="소유자",
    )
    title = models.CharField("제목", max_length=120)
    prompt = models.TextField("생성 프롬프트", blank=True)
    image = models.ImageField("이미지 파일", upload_to="img/%Y/%m/", blank=True, null=True)
    image_url = models.URLField("외부 이미지 URL", blank=True)
    created_at = models.DateTimeField("생성일시", auto_now_add=True)

    class Meta:
        db_table = "img"
        ordering = ("-created_at",)
        verbose_name = "이미지"
        verbose_name_plural = "이미지"

    def __str__(self) -> str:
        return f"[{self.pk}] {self.title}"

    @property
    def display_url(self) -> str:
        """템플릿에서 사용할 단일 URL (업로드 우선, 없으면 외부 URL)."""
        if self.image:
            return self.image.url
        return self.image_url


class ImgUsed(models.Model):
    """이미지가 사용된 이력 1건.

    DB table: img_used
    """

    class UsedIn(models.TextChoices):
        CHAT_CHAR = "chat_char", "독대 모드 채팅"
        CHAT_SCENE = "chat_scene", "역할극 모드 채팅"
        OTHER = "other", "기타"

    img = models.ForeignKey(
        Img,
        on_delete=models.CASCADE,
        related_name="usages",
        verbose_name="이미지",
    )
    used_in = models.CharField(
        "사용 영역", max_length=20, choices=UsedIn.choices, default=UsedIn.CHAT_CHAR
    )
    ref_id = models.CharField("참조 ID", max_length=64, blank=True)
    used_at = models.DateTimeField("사용일시", auto_now_add=True)

    class Meta:
        db_table = "img_used"
        ordering = ("-used_at",)
        verbose_name = "이미지 사용 이력"
        verbose_name_plural = "이미지 사용 이력"

    def __str__(self) -> str:
        return f"{self.img_id} @ {self.get_used_in_display()}"
