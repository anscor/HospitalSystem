# Generated by Django 3.0 on 2019-12-18 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medicine", "0003_auto_20191215_2149"),
    ]

    operations = [
        migrations.AddField(
            model_name="medicinehandoutrecord",
            name="is_handout",
            field=models.BooleanField(default=1, verbose_name="是否已经发放"),
        ),
    ]
