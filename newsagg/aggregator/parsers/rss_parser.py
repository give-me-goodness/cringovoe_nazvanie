import feedparser
import requests
from datetime import datetime
from typing import List, Dict
from .base_parser import BaseParser


class RSSParser(BaseParser):
    """Парсер RSS-лент"""

    def parse(self) -> List[Dict]:
        try:
            print(f"Парсим RSS: {self.source.name}")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            feed = feedparser.parse(self.source.url, request_headers=headers)

            if feed.bozo:
                print(f"Ошибка RSS для {self.source.name}: {feed.bozo_exception}")
                return []

            news_items = []

            for entry in feed.entries[:25]:
                try:
                    news_data = {
                        'title': entry.title,
                        'content': self._get_content(entry),
                        'url': entry.link,
                        'published_date': self._parse_date(entry),
                        'summary': self._get_summary(entry),
                        'media': False,
                        'media_type': 'none'
                    }
                    news_items.append(news_data)
                except Exception as e:
                    print(f"Ошибка обработки новости: {e}")
                    continue

            print(f"RSS {self.source.name}: найдено {len(news_items)} новостей")
            return news_items

        except Exception as e:
            print(f"Критическая ошибка RSS парсинга {self.source.name}: {e}")
            return []

    def _get_content(self, entry):
        """Получаем контент новости"""
        if hasattr(entry, 'content') and entry.content:
            return entry.content[0].value
        elif hasattr(entry, 'summary'):
            return entry.summary
        elif hasattr(entry, 'description'):
            return entry.description
        return entry.title

    def _get_summary(self, entry):
        """Создаем краткое описание"""
        content = self._get_content(entry)
        if content and len(content) > 200:
            return content[:200] + '...'
        return content or ''

    def _parse_date(self, entry):
        """Парсим дату публикации"""
        date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']

        for field in date_fields:
            if hasattr(entry, field) and getattr(entry, field):
                date_tuple = getattr(entry, field)
                return datetime(*date_tuple[:6])

        return datetime.now()