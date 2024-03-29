# Generated by Django 3.0 on 2019-12-16 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("laboratory", "0003_auto_20191216_2249"),
    ]

    operations = [
        migrations.AddField(
            model_name="laboratorytype",
            name="create_time",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="创建时间",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="laboratorytype",
            name="creator",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="created_laboratory_types",
                to=settings.AUTH_USER_MODEL,
                verbose_name="创建者id",
            ),
            preserve_default=False,
        ),
    ]
