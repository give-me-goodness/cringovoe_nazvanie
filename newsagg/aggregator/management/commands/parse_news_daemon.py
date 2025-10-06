import time
import schedule
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

from aggregator.parsers.parser_manager import ParserManager
from aggregator.models import NewsItem


class Command(BaseCommand):
    help = "Непрерывный парсинг на сервере"

    def add_arguments(self, parser):
        parser.add_argument(
            "--interval",
            type=int,
            default=120,
            help="Интервал парсинга: 120 минут"
        )
        parser.add_argument(
            "--cleanup-days",
            type=int,
            default=2,
            help="Удалять новости старше 2 дней"
        )

    def handle(self, *args, **options):
        interval_minutes = options["interval"]
        cleanup_days = options["cleanup_days"]

        self.stdout.write(
            self.style.SUCCESS(
                f"Запускаем демон парсера\n"
                f"Интервал: {interval_minutes} минут\n"
                f"Очистка: каждые {cleanup_days} дней\n"
                f"Остановка: Ctrl+C"
            )
        )

        self.parse_and_cleanup(cleanup_days)

        schedule.every(interval_minutes).minutes.do(
            self.parse_and_cleanup, cleanup_days
        )

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Демон остановлен"))

    def parse_and_cleanup(self, cleanup_days):
        """Парсинг и очистка старых новостей"""

        self.stdout.write(f"{timezone.now().strftime('%Y-%m-%d %H:%M')} - Запуск парсинга...")

        try:
            parser_manager = ParserManager()
            new_news = parser_manager.parse_all_sources()

            cutoff_date = timezone.now() - timedelta(days=cleanup_days)
            old_news = NewsItem.objects.filter(created_at__lt=cutoff_date)
            deleted_count = old_news.count()

            with transaction.atomic():
                old_news.delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Цикл завершен: добавлено {new_news} новостей, удалено {deleted_count} старых"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка в цикле: {e}")
            )
