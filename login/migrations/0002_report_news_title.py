# Generated by Django 5.1 on 2024-10-21 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="news_title",
            field=models.TextField(default="Nothing"),
        ),
    ]
