from django.contrib import admin

from .models import CustomFieldType, CustomField, Section, Entry


@admin.register(CustomFieldType)
class CustomFieldTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "order_id"]
    fieldsets = [
        (None, {
            'fields': ["name", "description"]
        }),
        ('Presentation', {
            'fields': [("name_plural", "order_id")]
        }),
    ]


@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "order_id"]
    list_filter = ["type"]
    fieldsets = [
        (None, {
            'fields': [("name", "type"), "value"]
        }),
        ('Presentation', {
            'fields': ["order_id"]
        }),
    ]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "order_id"]
    fieldsets = [
        (None, {
            'fields': ["name", "description"]
        }),
        ('Presentation', {
            'fields': ["order_id"]
        }),
    ]


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ["name", "section", "order_id", "publish"]
    list_filter = ["section", "publish"]
    fieldsets = [
        (None, {
            'fields': [("name", "publish"), "value"]
        }),
        ('Custom Fields', {
            'fields': ["custom_fields_presentation_order", "custom_fields"]
        }),
        ('Presentation', {
            'fields': [("section", "order_id")]
        }),
        ('User tracking', {
            'fields': ["favorite_by"]
        }),
    ]
    filter_horizontal = ["custom_fields_presentation_order", "custom_fields", "favorite_by"]
