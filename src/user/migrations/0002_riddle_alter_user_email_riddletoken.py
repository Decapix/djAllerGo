# Generated by Django 5.0 on 2023-12-21 16:35

import django.db.models.deletion
import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Riddle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('correct_answer', models.CharField(max_length=25)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=user.models.NullableUniqueEmailField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='RiddleToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('riddle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.riddle')),
            ],
        ),
    ]
