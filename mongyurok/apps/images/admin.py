from django.contrib import admin

from .models import Img, ImgUsed


class ImgUsedInline(admin.TabularInline):
    model = ImgUsed
    extra = 0


@admin.register(Img)
class ImgAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "created_at")
    search_fields = ("title", "prompt")
    inlines = [ImgUsedInline]


@admin.register(ImgUsed)
class ImgUsedAdmin(admin.ModelAdmin):
    list_display = ("id", "img", "used_in", "ref_id", "used_at")
    list_filter = ("used_in",)
