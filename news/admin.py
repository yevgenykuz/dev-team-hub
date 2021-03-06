from django.contrib import admin

from .models import Tag, Article


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "publish", "display_tags", "created_by", "created_on")
    list_filter = ("tags", "publish", "created_on", "created_by")
    fields = [("title", "created_by", "publish"), "body", "tags"]
    filter_horizontal = ["tags"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # update "created_by" field with current user automatically
        if db_field.name == 'created_by':
            kwargs['initial'] = request.user.id
        return super(ArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
