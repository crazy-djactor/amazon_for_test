from django.db import models

# Create your models here.
from django.db import models
# Create your models here.


class Snippet(models.Model):
    serial_num = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    date_time = models.DateTimeField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Snippet'
