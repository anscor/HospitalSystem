# Generated by Django 3.0 on 2019-12-15 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservation", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="is_paid",
            field=models.BooleanField(
                choices=[(0, "否"), (1, "是")], default=0, verbose_name="是否已经缴费"
            ),
        ),
    ]
