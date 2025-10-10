from typing import List
from django.utils import timezone
from aggregator.models import NewsSource
from .rss_parser import RSSParser
import asyncio


class ParserManager:
    """Упрощенный менеджер парсеров только с RSS"""

    def __init__(self):
        self.parsers = {
            'rss': RSSParser,
        }

    def get_parser(self, source: NewsSource):
        parser_class = self.parsers.get(source.source_type)
        if parser_class:
            return parser_class(source)
        return None

    def parse_all_sources(self) -> int:
        """Синхронный парсинг всех источников"""
        import time
        start_time = time.time()

        try:
            active_sources = NewsSource.objects.filter(is_active=True)
            print(f"Запуск парсинга {len(active_sources)} RSS источников...")

            total_news = 0

            for source in active_sources:
                parser = self.get_parser(source)
                if parser:
                    try:
                        news_items = parser.parse()
                        saved_count = 0

                        for news_data in news_items:
                            if parser.save_news_item(news_data):
                                saved_count += 1

                        source.last_parsed = timezone.now()
                        source.save()

                        print(f"{source.name}: {saved_count} новостей")
                        total_news += saved_count

                    except Exception as e:
                        print(f"Ошибка парсинга {source.name}: {e}")

            duration = time.time() - start_time
            print(f"Парсинг завершен! {total_news} новостей за {duration:.1f} секунд")
            return total_news

        except Exception as e:
            print(f"Критическая ошибка парсинга: {e}")
            return 0
