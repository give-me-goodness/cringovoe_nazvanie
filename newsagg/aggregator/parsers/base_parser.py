import abc
import logging
from typing import Dict, List, Optional

from aggregator.models import NewsItem

logger = logging.getLogger(__name__)


class BaseParser(abc.ABC):
    """Абстрактный базовый парсер."""

    def __init__(self, source):
        self.source = source
        self.name = "BaseParser"

    @abc.abstractmethod
    def parse(self) -> List[Dict]:
        """Основной метода парсинга - его описываем в дочерках."""
        pass

    def clean_text(self, text: str) -> str:
        """Очистка текста от лишних пробелов и символов"""
        if not text:
            return ""
        return ' '.join(text.split())

    def save_news_item(self, news_data: Dict) -> Optional["NewsItem"]:

        try:
            if NewsItem.objects.filter(url=news_data["url"]).exists():
                return None

            news_item = NewsItem.objects.create(
                title=news_data["title"],
                content=news_data["content"],
                source=self.source,
                url=news_data["url"],
                published_date=news_data["published_date"],
                summary=news_data.get('summary', ''),
                media=news_data.get('media', False),
                media_type=news_data.get('media_type', 'none')
            )
            logger.info(f"Новость сохранена: {news_data['title'][:100]}")
            return news_item

        except Exception as e:
            logger.error(f'Ошибка сохранения новости: {e}')
            return None
