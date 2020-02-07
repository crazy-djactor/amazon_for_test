import threading

from django.db import models
# Create your models here.

class Snippet(models.Model):
    serial_num = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    date_time = models.DateTimeField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'snippet'
        verbose_name_plural = "Snippet"


class SnippetHistory(models.Model):
    serial_num = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    date_time = models.DateTimeField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'snippet_history'
        verbose_name_plural = "Snippet"