# Generated by Django 5.0 on 2023-12-28 10:48

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_contact_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(default='FR', max_length=2),
        ),
    ]
