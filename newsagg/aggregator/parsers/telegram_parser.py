import asyncio
import os
from datetime import datetime, timedelta
from typing import List, Dict
from django.core.files.base import ContentFile

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
                        limit=50,
                        offset_date=since_date
                    ):
                        if message.text and len(message.text.strip()) > 50:
                            media, media_type, media_files = await self._process_media(message)
                            news_data = {
                                'title': self._generate_title(message.text),
                                'content': self.clean_text(message.text),
                                'url': f"https://t.me/{self.source.username}/{message.id}",
                                'published_date': message.date,
                                'summary': self._generate_summary(message.text),
                                'media': media,
                                'media_type': media_type,
                                'media_files': media_files
                            }
                            news_items.append(news_data)

                    print(f"Telegram: найдено {len(news_items)} новостей из {self.source.name}")
                except ChannelPrivateError:
                    print(f"Канал {self.source.username} приватный или недоступен")
        except Exception as e:
            print(f"Ошибка Telegram парсинга {self.source.name}: {e}")

        return news_items

    async def _process_media(self, message) -> tuple:
        """Обработка медиафайлов сообщения"""
        media = False
        media_type = 'none'
        media_files = []

        try:
            if message.media:
                media = True

                if hasattr(message.media, 'photo'):
                    media_type = 'image'
                    media_files = await self._download_media(message, 'image')

                elif (hasattr(message.media, 'document') and 
                      hasattr(message.media.document, 'mime_type') and
                      message.media.document.mime_type.startswith('video')):
                    media_type = 'video'
                    media_files = await self._download_media(message, 'video')

                elif hasattr(message.media, 'document'):
                    print(f"Пропускаем документ: {getattr(message.media.document, 'mime_type', 'unknown')}")

        except Exception as e:
            print(f"Ошибка обработки медиа: {e}")

        return media, media_type, media_files

    async def _download_media(self, message, file_type: str) -> List[Dict]:
        """Скачивание медиафайлов"""
        media_files = []

        try:
            MAX_FILE_SIZE = 10 * 1024 * 1024

            if hasattr(message.media, 'document') and message.media.document.size > MAX_FILE_SIZE:
                print(f"⚠️ Файл слишком большой: {message.media.document.size} bytes")
                return media_files

            file_data = await message.download_media(file=bytes)

            if file_data:
                extension = self._get_file_extension(message, file_type)
                filename = f"{message.id}_{file_type}{extension}"

                media_files.append({
                    'file_data': file_data,
                    'filename': filename,
                    'file_type': file_type,
                    'file_size': len(file_data),
                    'file_url': f"https://t.me/{self.source.username}/{message.id}"
                })

                print(f"Скачано {file_type}: {len(file_data)} bytes")

        except Exception as e:
            print(f"Ошибка скачивания {file_type}: {e}")

        return media_files

    def _get_file_extension(self, message, file_type: str) -> str:
        """Определение расширения файла"""
        if file_type == 'image':
            return '.jpg'
        elif file_type == 'video':
            if (hasattr(message.media, 'document') and hasattr(message.media.document, 'mime_type')):
                if 'mp4' in message.media.document.mime_type:
                    return '.mp4'
                elif 'quicktime' in message.media.document.mime_type:
                    return '.mov'
            return '.mp4'
        return ''

    def save_news_item(self, news_data: Dict):
        """Переопределяем сохранение для обработки медиа"""
        from aggregator.models import NewsItem, MediaFile

        try:
            news_item = super().save_news_item(news_data)
            if not news_item:
                return None

            if news_data.get('media') and news_data.get('media_files'):
                for media_file in news_data['media_files']:
                    try:
                        # Создаем Django File объект из бинарных данных
                        django_file = ContentFile(
                            media_file['file_data'], 
                            name=media_file['filename']
                        )

                        MediaFile.objects.create(
                            news=news_item,
                            file=django_file,
                            file_url=media_file['file_url'],
                            file_type=media_file['file_type'],
                            file_size=media_file['file_size']
                        )

                        print(f"Сохранен {media_file['file_type']} файл")

                    except Exception as e:
                        print(f"Ошибка сохранения медиафайла: {e}")

            return news_item

        except Exception as e:
            print(f"Ошибка сохранения новости с медиа: {e}")
            return None

    def _generate_title(self, text: str) -> str:
        """Генерация заголовка из текста сообщения"""
        return text[:50].strip() + ('...' if len(text) > 50 else '')

    def _generate_summary(self, text: str) -> str:
        """Генерация краткого описания (2-3 предложения)"""
        sentences = text.split('.')
        summary = '.'.join(sentences[:3]) + '.'
        return summary[:200] + ('...' if len(summary) > 200 else '')