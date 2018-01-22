from django.contrib import admin

from .models import CustomLink, SiteConfig


@admin.register(CustomLink)
class CustomLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order_id")
    fields = [("name", "order_id"), "url"]


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "current_release_version", "display_links")
    filter_horizontal = ["custom_links"]

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)
