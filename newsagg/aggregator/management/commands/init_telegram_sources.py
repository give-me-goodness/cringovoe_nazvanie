from django.core.management.base import BaseCommand
from aggregator.models import NewsSource


class Command(BaseCommand):
    help = 'Добавление Telegram каналов для парсинга'

    def handle(self, *args, **options):
        telegram_channels = [
            {'name': 'РИА Новости', 'username': 'rian_ru'},
            {'name': 'РБК', 'username': 'rbc_news'},
            {'name': 'RT', 'username': 'rt_russian'},
            {'name': 'Ведомости', 'username': 'vedomosti'},
            {'name': 'Фонтанка', 'username': 'fontankaspb'},
            {'name': 'BBC Russian', 'username': 'bbcrussian'},
            {'name': 'ТАСС', 'username': 'tass_agency'},
            {'name': 'Reuters', 'username': 'reuters_russia'},
            {'name': 'Интерфакс', 'username': 'interfaxonline'},
            {'name': 'Meduza', 'username': 'meduzalive'},
            {'name': 'SVTV NEWS', 'username': 'svtvnews'},
            {'name': 'Медиазона', 'username': 'mediazzzona'},
            {'name': 'Новая газета Европа', 'username': 'novaya_europe'},
            {'name': 'Радио Свобода', 'username': 'radiosvoboda'},
            {'name': 'ASTRA', 'username': 'astrapress'},
            {'name': 'Mash', 'username': 'breakingmash'},
            {'name': 'Readovka', 'username': 'readovkanews'},
        ]

        for channel_data in telegram_channels:
            url = f"https://t.me/{channel_data['username']}"

            source, created = NewsSource.objects.get_or_create(
                username=channel_data['username'],
                defaults={
                    'name': channel_data['name'],
                    'url': url,
                    'source_type': 'telegram',
                    'is_active': True
                }
            )

            if created:
                self.stdout.write(f"Добавлен канал: {channel_data['name']} (@{channel_data['username']})")
            else:
                self.stdout.write(f"Канал уже существует: {channel_data['name']}")
