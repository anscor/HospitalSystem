from outpatient.models import Prescription

from django.db import models
from django.contrib.auth.models import User


class MedicineType(models.Model):
    name = models.CharField(max_length=256, verbose_name="类型名")

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_medicine_types",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modifier = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="modified_medicine_types",
        verbose_name="修改者id",
    )
    modify_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="修改时间"
    )

    class Meta:
        verbose_name = "药物类型"
        verbose_name_plural = "药物类型"
        db_table = "medicine_type"


class Medicine(models.Model):
    medicine_type = models.ForeignKey(
        MedicineType,
        on_delete=models.DO_NOTHING,
        related_name="medicine",
        verbose_name="药物类型id",
    )

    name = models.CharField(max_length=256, verbose_name="药物名")
    in_price = models.FloatField(verbose_name="进货价")
    price = models.FloatField(verbose_name="单价")
    count = models.IntegerField(verbose_name="库存数量")

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_medicine",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modifier = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="modified_medicine",
        verbose_name="修改者id",
    )
    modify_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="修改时间"
    )

    class Meta:
        verbose_name = "药物"
        verbose_name_plural = "药物"
        db_table = "medicine"


class MedicineHandoutRecord(models.Model):
    # 表示是根据哪个处方来进行发放药物的
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.DO_NOTHING,
        related_name="medicine_handout_records",
        verbose_name="处方id",
    )

    # 药房工作人员
    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_medicine_handout_records",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "药物发放记录"
        verbose_name_plural = "药物发放记录"
        db_table = "medicine_handout_record"
