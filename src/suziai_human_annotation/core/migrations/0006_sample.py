# Generated by Django 5.1.4 on 2024-12-31 18:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_choices"),
    ]

    operations = [
        migrations.AddField(
            model_name="sample",
            name="group",
            field=models.SmallIntegerField(default=0),
        ),
    ]
