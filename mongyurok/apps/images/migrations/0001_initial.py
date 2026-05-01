"""이미지/이미지 사용 이력 초기 마이그레이션."""
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Img",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=120, verbose_name="제목")),
                ("prompt", models.TextField(blank=True, verbose_name="생성 프롬프트")),
                ("image", models.ImageField(blank=True, null=True, upload_to="img/%Y/%m/", verbose_name="이미지 파일")),
                ("image_url", models.URLField(blank=True, verbose_name="외부 이미지 URL")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="생성일시")),
                ("owner", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="images", to=settings.AUTH_USER_MODEL, verbose_name="소유자")),
            ],
            options={
                "verbose_name": "이미지",
                "verbose_name_plural": "이미지",
                "db_table": "img",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="ImgUsed",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("used_in", models.CharField(choices=[("chat_char", "독대 모드 채팅"), ("chat_scene", "역할극 모드 채팅"), ("other", "기타")], default="chat_char", max_length=20, verbose_name="사용 영역")),
                ("ref_id", models.CharField(blank=True, max_length=64, verbose_name="참조 ID")),
                ("used_at", models.DateTimeField(auto_now_add=True, verbose_name="사용일시")),
                ("img", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="usages", to="images.img", verbose_name="이미지")),
            ],
            options={
                "verbose_name": "이미지 사용 이력",
                "verbose_name_plural": "이미지 사용 이력",
                "db_table": "img_used",
                "ordering": ("-used_at",),
            },
        ),
    ]
