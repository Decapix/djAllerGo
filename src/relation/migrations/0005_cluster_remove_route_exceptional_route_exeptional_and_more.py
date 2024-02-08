# Generated by Django 5.0 on 2024-01-25 15:04

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("relation", "0004_route_exceptional"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cluster",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("centre_latitude_depart", models.FloatField()),
                ("centre_longitude_depart", models.FloatField()),
                ("centre_latitude_arrivee", models.FloatField()),
                ("centre_longitude_arrivee", models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name="route",
            name="exceptional",
        ),
        migrations.AddField(
            model_name="route",
            name="exeptional",
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="route",
            name="cluster",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="relation.cluster",
            ),
        ),
    ]
