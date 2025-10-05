from django.contrib import admin
from .models import NewsSource, NewsItem


@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "source_type", "is_active", "last_parsed")
    list_filter = ("source_type", "is_active")
    search_fields = ("name", "username")


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "published_date", "is_processed")
    list_filter = ("source", "is_processed", "published_date")
    search_fields = ("title", "summary", "content")
