from django.shortcuts import render, get_object_or_404
from .models import NewsItem


def news_list(request):
    """Главная страница с лентой новостей"""
    news = NewsItem.objects.select_related("source").all()[:20]  # первые 20
    return render(request, "aggregator/news_list.html", {"news": news})


def news_detail_card(request, pk):
    """HTML для модалки с подробной новостью"""
    news = get_object_or_404(NewsItem, pk=pk)
    return render(request, "aggregator/news_card.html", {"item": news})
