# Generated by Django 5.0 on 2023-12-31 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0003_route_departure_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='exceptional',
            field=models.BooleanField(null=True),
        ),
    ]
