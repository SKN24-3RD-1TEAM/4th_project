"""이미지 페이지용 템플릿 헬퍼."""
from django import template

register = template.Library()


@register.filter
def initial(value: str) -> str:
    """이름의 첫 글자 반환 (사이드바 아바타용)."""
    if not value:
        return ""
    return value[0]
