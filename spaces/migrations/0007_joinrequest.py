# Generated by Django 5.0.3 on 2024-04-06 11:51

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spaces", "0006_alter_notice_created_at_alter_notice_deadline"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="JoinRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "request_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("is_rejected", models.BooleanField(default=False)),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                ("is_pending", models.BooleanField(default=True)),
                (
                    "space",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="spaces.space",
                        to_field="spaceId",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
