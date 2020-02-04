# Generated by Django 3.0.3 on 2020-02-04 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_num', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(blank=True, max_length=255, null=True)),
                ('date_time', models.DateTimeField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'Snippet',
            },
        ),
    ]