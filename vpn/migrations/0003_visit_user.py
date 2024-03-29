# Generated by Django 5.0.1 on 2024-01-24 10:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vpn", "0002_remove_visit_page_transitions_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="visit",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="visits",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
