# Generated by Django 4.2.6 on 2023-11-03 12:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("polls", "0004_alter_poll_pub_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="owner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="poll",
            name="pub_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 3, 12, 47, 15, 681083, tzinfo=datetime.timezone.utc
                ),
                verbose_name="date published",
            ),
        ),
    ]