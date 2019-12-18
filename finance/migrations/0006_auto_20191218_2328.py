# Generated by Django 3.0 on 2019-12-18 23:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0005_refundrecorditem_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audititem',
            name='receive',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='audit_items', to='finance.PayRecord', verbose_name='收款条目id'),
        ),
        migrations.AlterField(
            model_name='audititem',
            name='refund',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='audit_items', to='finance.RefundRecord', verbose_name='退款条目'),
        ),
        migrations.AlterField(
            model_name='auditrecord',
            name='audit_time',
            field=models.DateTimeField(auto_now=True, verbose_name='审核时间'),
        ),
        migrations.AlterField(
            model_name='auditrecord',
            name='auditor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='audited_records', to=settings.AUTH_USER_MODEL, verbose_name='审核者id'),
        ),
    ]
