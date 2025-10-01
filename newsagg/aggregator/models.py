from django.db import models


class NewsSource(models.Model):
    """Хранение новостей"""
    SOURCE_TYPES = [
        ('telegram', 'Telegram'),
    ]
    name = models.CharField(max_length=200, verbose_name="Название канала")
    username = models.CharField(max_length=100, verbose_name="Username канала")
    url = models.URLField(verbose_name="URL канала", blank=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES, default='telegram', verbose_name="Тип источника")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    last_parsed = models.DateTimeField(null=True, blank=True, verbose_name="Последний парсинг")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Источник новостей"
        verbose_name_plural = "Источники новостей"


class NewsItem(models.Model):
    """Хранение новостей"""
    title = models.CharField(max_length=500, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Полный текст")
    summary = models.TextField(blank=True, verbose_name="Краткое описание")
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, verbose_name="Источник")
    url = models.URLField(unique=True, verbose_name="Ссылка на новость")
    published_date = models.DateTimeField(verbose_name="Дата публикации")
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    def __str__(self):
        return self.title[:100]

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['published_date']),
            models.Index(fields=['source', 'published_date']),
        ]
