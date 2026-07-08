from django.contrib import admin
from .models import PromptLog

@admin.register(PromptLog)
class PromptLogAdmin(admin.ModelAdmin):
    list_display = (
        "prompt_text",
        "detection_type",
        "status",
        "confidence",
        "created_at",
    )
    list_filter = ("status", "detection_type", "created_at")
    search_fields = ("prompt_text",)
    ordering = ("-created_at",)