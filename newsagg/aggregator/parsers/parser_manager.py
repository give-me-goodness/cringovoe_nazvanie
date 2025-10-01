from django.utils import timezone
from aggregator.models import NewsSource

from .telegram_parser import TelegramParser


class ParserManager:
    """Менеджер для управления парсерами"""

    def __init__(self):
        self.parsers = {
            'telegram': TelegramParser,
        }

    def get_parser(self, source: NewsSource):
        """Получение парсера для источника"""
        parser_class = self.parsers.get(source.source_type)
        if parser_class:
            return parser_class(source)
        return None

    def parse_all_sources(self) -> int:
        """Парсинг всех активных источников"""
        total_news = 0
        active_sources = NewsSource.objects.filter(is_active=True)

        print(f"Начинаем парсинг {active_sources.count()} источников...")

        for source in active_sources:
            parser = self.get_parser(source)
            if parser:
                try:
                    news_items = parser.parse()
                    for news_data in news_items:
                        parser.save_news_item(news_data)
                    total_news += len(news_items)

                    source.last_parsed = timezone.now()
                    source.save()

                    print(f"{source.name}: обработано {len(news_items)} новостей")

                except Exception as e:
                    print(f"Ошибка парсинга {source.name}: {e}")

        print(f"Парсинг завершен! Всего добавлено {total_news} новостей")
        return total_news
