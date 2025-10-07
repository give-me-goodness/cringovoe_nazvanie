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
    media = models.BooleanField(default=False, verbose_name="Медиа")
    media_type = models.CharField(max_length=10, choices=[
        ('image', 'Изображение'),
        ('video', 'Видео'),
        ('none', 'Без медиа')
    ], default="none", verbose_name="Тип медиа")

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


class MediaFile(models.Model):
    """Хранение медиафайлов"""
    news = models.ForeignKey(NewsItem, on_delete=models.CASCADE, related_name='media_files', verbose_name="Новость")
    file = models.FileField(upload_to='news_media/%Y/%m/%d/', blank=True, null=True, verbose_name="Файл")
    file_url = models.URLField(verbose_name="Ссылка", blank=True)
    file_type = models.CharField(max_length=20, choices=[
        ('image', 'Изображение'),
        ('video', 'Видео'),
        ('document', 'Документ'),
        ('audio', 'Аудио')
    ], verbose_name="Тип файла")
    file_size = models.IntegerField(default=0, verbose_name="Размер файла")
    thumbnail = models.ImageField(upload_to='media_thumbnails/', blank=True, null=True, verbose_name="Превью")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.file_type} - {self.news.title[:50]}"

    class Meta:
        verbose_name = "Медиафайл"
        verbose_name_plural = "Медиафайлы"
        indexes = [
            models.Index(fields=['news', 'file_type']),
        ]

    @property
    def file_size_mb(self):
        """Размер файла"""
        return round(self.file_size / (1024 * 1024), 2) if self.file_size else 0

    @property
    def is_image(self):
        return self.file_type == 'image'

    @property
    def is_video(self):
        return self.file_type == 'video'
