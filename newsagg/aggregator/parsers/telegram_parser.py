import asyncio
from datetime import datetime, timedelta
from typing import List, Dict

from .base_parser import BaseParser


class TelegramParser(BaseParser):
    """Парсер Telegram каналов"""

    def __init__(self, source):
        super().__init__(source)
        self.api_id = "25958394"
        self.api_hash = "e8e5db077b49e97192f08cd90a9494b2"

    def parse(self) -> List[Dict]:
        """Синхронный метод парсинга (запускает асинхронный)"""
        try:
            return asyncio.run(self._async_parse())
        except Exception as e:
            print(f"Ошибка парсинга Telegram: {e}")
            return []

    async def _async_parse(self) -> List[Dict]:
        """Асинхронный парсинг Telegram канала"""
        news_items = []

        try:
            from telethon import TelegramClient
            from telethon.errors import ChannelPrivateError

            # Настройки Telegram API (вынеси в settings.py позже)

            client = TelegramClient('session_name', self.api_id, self.api_hash)

            async with client:
                since_date = datetime.now() - timedelta(hours=24)

                try:
                    async for message in client.iter_messages(
                        self.source.username,
                        limit=100,
                        offset_date=since_date
                    ):
                        if message.text and len(message.text.strip()) > 50:
                            news_data = {
                                'title': self._generate_title(message.text),
                                'content': self.clean_text(message.text),
                                'url': f"https://t.me/{self.source.username}/{message.id}",
                                'published_date': message.date,
                                'summary': self._generate_summary(message.text)
                            }
                            news_items.append(news_data)

                    print(f"Telegram: найдено {len(news_items)} новостей из {self.source.name}")
                except ChannelPrivateError:
                    print(f"Канал {self.source.username} приватный или недоступен")
        except Exception as e:
            print(f"Ошибка Telegram парсинга {self.source.name}: {e}")

        return news_items

    def _generate_title(self, text: str) -> str:
        """Генерация заголовка из текста сообщения"""
        return text[:50].strip() + ('...' if len(text) > 50 else '')

    def _generate_summary(self, text: str) -> str:
        """Генерация краткого описания (2-3 предложения)"""
        sentences = text.split('.')
        summary = '.'.join(sentences[:3]) + '.'
        return summary[:200] + ('...' if len(summary) > 200 else '')