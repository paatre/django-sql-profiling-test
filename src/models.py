from django.db import models


class LargeTable(models.Model):
    name = models.CharField(max_length=100, blank=True)
    processed = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
