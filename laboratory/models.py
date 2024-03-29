from django.db import models
from django.contrib.auth.models import User, Group

from finance.models import PayRecord


class Laboratory(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="laboratories",
        verbose_name="病人id",
    )
    executor = models.ForeignKey(
        Group,
        on_delete=models.DO_NOTHING,
        related_name="executed_laboratories",
        verbose_name="执行科室id",
    )

    pay = models.OneToOneField(
        PayRecord,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="laboratory",
        verbose_name="缴费记录id",
    )

    # 一般为医生
    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_laboratories",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "化验单"
        verbose_name_plural = "化验单"
        db_table = "laboratory"


class LaboratoryType(models.Model):
    name = models.CharField(max_length=256, verbose_name="类型名称")
    price = models.FloatField(verbose_name="价格")

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_laboratory_types",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "化验类型"
        verbose_name_plural = "化验类型"
        db_table = "laboratory_type"


class LaboratoryItem(models.Model):
    laboratory = models.ForeignKey(
        Laboratory,
        on_delete=models.DO_NOTHING,
        related_name="items",
        verbose_name="化验单id",
    )
    laboratory_type = models.ForeignKey(
        LaboratoryType,
        on_delete=models.DO_NOTHING,
        related_name="items",
        verbose_name="化验类型id",
    )

    commet = models.CharField(
        max_length=64, null=True, blank=True, verbose_name="注意事项"
    )
    check_part = models.CharField(
        max_length=64, null=True, blank=True, verbose_name="检查部位"
    )

    class Meta:
        verbose_name = "化验单项目"
        verbose_name_plural = "化验单项目"
        db_table = "laboratory_item"
