# Generated by Django 3.0 on 2019-12-16 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("finance", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payrecord",
            name="modifier",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="modified_pay_records",
                to=settings.AUTH_USER_MODEL,
                verbose_name="修改者id",
            ),
        ),
        migrations.AddField(
            model_name="payrecord",
            name="modify_time",
            field=models.DateTimeField(auto_now=True, verbose_name="修改时间"),
        ),
        migrations.AlterField(
            model_name="payrecord",
            name="method",
            field=models.IntegerField(
                choices=[
                    (0, "未付款"),
                    (1, "现金"),
                    (2, "银联"),
                    (3, "支付宝"),
                    (4, "微信"),
                ],
                default=0,
                verbose_name="收款方式",
            ),
        ),
        migrations.AlterField(
            model_name="payrecord",
            name="receive",
            field=models.FloatField(blank=True, null=True, verbose_name="收款金额"),
        ),
        migrations.AlterField(
            model_name="payrecord",
            name="refund",
            field=models.FloatField(blank=True, null=True, verbose_name="找零"),
        ),
        migrations.AlterField(
            model_name="refundrecord",
            name="method",
            field=models.IntegerField(
                choices=[
                    (0, "未付款"),
                    (1, "现金"),
                    (2, "银联"),
                    (3, "支付宝"),
                    (4, "微信"),
                ],
                default=0,
                verbose_name="退款方式",
            ),
        ),
    ]
