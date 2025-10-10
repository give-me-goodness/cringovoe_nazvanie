from django.core.management.base import BaseCommand
from aggregator.models import NewsSource


class Command(BaseCommand):
    help = 'Добавление RSS источников для парсинга'

    def handle(self, *args, **options):
        rss_sources = [
            {'name': 'РИА Новости', 'url': 'https://ria.ru/export/rss2/archive/index.xml'},
            {'name': 'ТАСС', 'url': 'https://tass.ru/rss/v2.xml'},
            {'name': 'РБК', 'url': 'https://rssexport.rbc.ru/rbcnews/news/30/full.rss'},
            {'name': 'Интерфакс', 'url': 'https://www.interfax.ru/rss.asp'},
            {'name': 'Лента.ру', 'url': 'https://lenta.ru/rss/news'},
            {'name': 'BBC Russian', 'url': 'https://feeds.bbci.co.uk/russian/rss.xml'},
            {'name': 'Reuters', 'url': 'https://feeds.reuters.com/reuters/UKTopNews'},
            {'name': 'Meduza', 'url': 'https://meduza.io/rss/all'},
            {'name': 'Фонтанка', 'url': 'https://www.fontanka.ru/fontanka.rss'},
            {'name': 'Коммерсант', 'url': 'https://www.kommersant.ru/RSS/news.xml'},
            {'name': 'Газета.Ru', 'url': 'https://www.gazeta.ru/export/rss/lenta.xml'},
            {'name': 'RT', 'url': 'https://russian.rt.com/rss/'},
            {'name': 'Ведомости', 'url': 'https://www.vedomosti.ru/rss/news.xml'},
            {'name': 'Радио Свобода', 'url': 'https://www.svoboda.org/api/z-rqie$pp'},
            {'name': 'Медиазона', 'url': 'https://zona.media/rss'},
            {'name': 'Новая газета Европа', 'url': 'https://novayagazeta.eu/rss'},
        ]

        for source_data in rss_sources:
            source, created = NewsSource.objects.get_or_create(
                url=source_data['url'],
                defaults={
                    'name': source_data['name'],
                    'source_type': 'rss',
                    'is_active': True
                }
            )

            if created:
                self.stdout.write(f"Добавлен RSS: {source_data['name']}")
            else:
                self.stdout.write(f"ℹRSS уже существует: {source_data['name']}")
