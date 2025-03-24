from django.core.management.base import BaseCommand
from src.models import LargeTable


class Command(BaseCommand):
    help = "Bulk-create dummy rows"

    def handle(self, *args, **options):
        total = 1_000_000
        batch = 10_000
        created = 0

        while created < total:
            objs = [
                LargeTable(name=f"row-{i}")
                for i in range(created, min(total, created + batch))
            ]
            LargeTable.objects.bulk_create(objs)
            created += len(objs)
            self.stdout.write(f"Created {created}/{total}")
