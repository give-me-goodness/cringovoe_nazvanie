from django.shortcuts import render, get_object_or_404
from .models import NewsItem, NewsSource

def news_list(request):
    """
    Главная страница с лентой новостей.
    Обрабатывает вкладки "Актуальное", "Лента" и фильтрацию по СМИ.
    """
    # Получаем все активные источники для кнопок фильтра
    sources = NewsSource.objects.filter(is_active=True).order_by('name')

    # Вкладка "Актуальное": 10 последних новостей (всегда, для full page)
    actual_news = NewsItem.objects.select_related("source").order_by('-published_date')[:10]

    # Вкладка "Лента": все новости (или отфильтрованные)
    source_filter = request.GET.get('source')
    if source_filter and source_filter != 'all':
        # Фильтруем по username источника
        lenta_news = NewsItem.objects.select_related("source").filter(source__username=source_filter).order_by('-published_date')
    else:
        # "Все" или без фильтра — все новости
        lenta_news = NewsItem.objects.select_related("source").order_by('-published_date')

    # Если это HTMX-запрос (клик по кнопке фильтра) и есть source-параметр,
    # то возвращаем только фрагмент HTML с отфильтрованной лентой (с лимитом для производительности).
    if request.headers.get('HX-Request') and 'source' in request.GET:
        lenta_news = lenta_news[:50]  # Лимит для partial (адаптируй)
        return render(request, 'aggregator/news_feed_lenta.html', {
            'lenta_news': lenta_news
        })

    # Для обычной загрузки страницы передаем все данные в главный шаблон
    context = {
        'sources': sources,
        'actual_news': actual_news,
        'lenta_news': lenta_news[:50],  # Лимит и для full page
        'active_filter': source_filter if source_filter != 'all' else None,  # Для подсветки (None для "Все")
    }
    return render(request, 'aggregator/news_list.html', context)


def news_detail_card(request, pk):
    """HTML для модалки с подробной новостью (без изменений)"""
    item = get_object_or_404(NewsItem, pk=pk)
    return render(request, "aggregator/news_card.html", {"item": item})