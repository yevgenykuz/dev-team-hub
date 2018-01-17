from django.contrib import admin

from .models import CustomFieldType, CustomField, Section, Entry


@admin.register(CustomFieldType)
class CustomFieldTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ["name", "type"]
    list_filter = ["type"]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ["name", "section", "published"]
    list_filter = ["section", "published"]
    fields = [("name", "published"), "section", "value", "custom_fields_presentation_order", "custom_fields"]
    filter_horizontal = ["custom_fields_presentation_order", "custom_fields"]
