# Generated by Django 5.0 on 2024-01-27 11:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("relation", "0007_rename_exeptional_route_exceptional"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cluster",
            name="cluster_label",
        ),
    ]
