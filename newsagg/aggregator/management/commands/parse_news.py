from django.core.management.base import BaseCommand
from django.utils import timezone
from aggregator.parsers.parser_manager import ParserManager


class Command(BaseCommand):
    help = 'Парсинг новостей из всех активных источников'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            help='Парсить только указанный источник (по имени)'
        )

    def handle(self, *args, **options):
        parser_manager = ParserManager()

        start_time = timezone.now()
        self.stdout.write(f"Начало парсинга в {start_time}")

        try:
            total_news = parser_manager.parse_all_sources()

            end_time = timezone.now()
            duration = (end_time - start_time).total_seconds()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Парсинг завершен. Добавлено {total_news} новостей за {duration:.2f} секунд"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка при парсинге: {e}")
            )
