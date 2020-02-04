from django.db import models
from rest_framework import serializers
from .models import Snippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    serial_num = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    date_time = models.DateTimeField(null=True)

    class Meta:
        model = Snippet
        fields = ['serial_num', 'code', 'date_time']

