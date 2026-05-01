"""이미지 페이지 뷰 (REQ-HIST-04 / SCR-LIST-IMG-01)."""
from django.db.models import Exists, OuterRef
from django.views.generic import ListView

from .models import Img, ImgUsed


class ImageListView(ListView):
    """사용된 적이 있는 이미지만 최신순으로 노출.

    - 1행 5열 그리드 (CSS Grid, 반응형으로 4/3/2열)
    - 카드 클릭 시 라이트박스(JS)로 원본 사이즈 확인
    """

    template_name = "images/image_list.html"
    context_object_name = "images"
    paginate_by = 30

    def get_queryset(self):
        used = ImgUsed.objects.filter(img=OuterRef("pk"))
        qs = (
            Img.objects.annotate(has_used=Exists(used))
            .filter(has_used=True)
            .order_by("-created_at")
        )
        # 로그인한 사용자가 있다면 본인 것만, 익명이면 데모용으로 전체 노출
        user = self.request.user
        if user.is_authenticated:
            qs = qs.filter(owner=user)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "이미지"
        ctx["page_description"] = "이미지를 클릭해 확인해 보세요"
        # 사이드바 더미 (실제로는 채팅 앱에서 가져옴)
        ctx["previous_chats"] = [
            {"name": "태조", "preview": "험준한 길로 향했네..."},
            {"name": "연산군", "preview": "일 조심하라 군네..."},
            {"name": "세조", "preview": "지금 뛰는는 것은..."},
        ]
        return ctx
