import time
from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext
from src.models import LargeTable


class Command(BaseCommand):
    help = "Profile batch update via OFFSET"

    def handle(self, *args, **options):
        batch_size = 10_000
        total = LargeTable.objects.count()
        offset = 0

        while offset < total:
            qs = LargeTable.objects.all()[offset : offset + batch_size]

            with CaptureQueriesContext(connection) as ctx:
                start = time.monotonic()
                pks = list(qs.values_list("id", flat=True))
                select_time = time.monotonic() - start

                start = time.monotonic()
                LargeTable.objects.filter(pk__in=pks).update(processed=True)
                update_time = time.monotonic() - start

            select_sql = next(
                (q for q in ctx.captured_queries if q["sql"].startswith("SELECT")), None
            )
            self.stdout.write(
                f"OFFSET {offset:,}: SELECT fetch={select_time:.3f}s (SQL reported {select_sql['time']}s), "
                f"UPDATE={update_time:.3f}s"
            )

            offset += batch_size
