# Generated by Django 3.0 on 2019-12-15 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payitem",
            name="price",
            field=models.FloatField(default=0, verbose_name="总价"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="paytype",
            name="modify_time",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="修改时间"
            ),
        ),
    ]
