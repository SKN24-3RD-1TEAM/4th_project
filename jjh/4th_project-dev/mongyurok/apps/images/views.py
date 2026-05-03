from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import GeneratedImage

# 좌측 사이드바에 보일 더미 이전 채팅 (정의서 화면 재현용)
PAST_CHATS = [
    {"id": "1", "name": "태조", "preview": "한양으로 천도하는 이야기를..."},
    {"id": "2", "name": "연산군", "preview": "갑자사화에 관한 글..."},
    {"id": "3", "name": "세종", "preview": "훈민정음 창제에 대한 글..."},
]


def image_page(request):
    """SCR-MAIN-05 이미지 화면."""
    images = GeneratedImage.objects.all()
    return render(
        request,
        "images/image_page.html",
        {"images": images, "past_chats": PAST_CHATS},
    )


@login_required
@require_POST
def upload_image(request):
    file = request.FILES.get("image")
    if file:
        GeneratedImage.objects.create(
            user=request.user,
            title=file.name,
            image=file,
        )
    return HttpResponseRedirect(reverse("images:image_page"))


@login_required
@require_POST
def delete_image(request, pk: int):
    image = get_object_or_404(GeneratedImage, pk=pk, user=request.user)
    image.image.delete(save=False)
    image.delete()
    return HttpResponseRedirect(reverse("images:image_page"))
