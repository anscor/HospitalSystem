from django.db import models

from django.contrib.auth.models import User, Group


class MedicalRecord(models.Model):
    # 病人
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="medical_records",
        verbose_name="病人id",
    )
    department = models.ForeignKey(
        Group,
        on_delete=models.DO_NOTHING,
        related_name="medical_records",
        verbose_name="就诊科室",
    )

    onset_date = models.DateField(verbose_name="发病日期")
    # 医生对病人病情诊断结果（是什么病，此项为比较简短的说明）
    diagnosis = models.CharField(max_length=255, verbose_name="诊断")
    # 医生对病情详细分析
    detail = models.TextField(null=True, blank=True, verbose_name="病情详情")
    # 病人自己对病情描述
    patient_description = models.TextField(
        null=True, blank=True, verbose_name="病人主诉"
    )
    onset_history = models.TextField(null=True, blank=True, verbose_name="发病史")
    time = models.DateTimeField(verbose_name="就诊时间")
    medicine_history = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="药物史"
    )
    # 指示此病人诊病过程是否结束，不可编辑表示此病人已诊断结束
    can_modify = models.BooleanField(verbose_name="是否可编辑")

    # 一般为医生
    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_medical_records",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 一般也为医生
    modifier = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="modified_medical_records",
        verbose_name="修改者id",
    )
    modify_time = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="修改时间"
    )

    class Meta:
        verbose_name = "病历"
        verbose_name_plural = "病历"
        db_table = "medical_record"


class Prescription(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="get_prescriptions",
        verbose_name="病人id",
    )

    IS_PAID = ((0, "未缴费"), (1, "已缴费"))
    is_paid = models.BooleanField(
        choices=IS_PAID, verbose_name="是否已经缴费", default=0
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_prescriptions",
        verbose_name="医生id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "处方"
        verbose_name_plural = "处方"
        db_table = "prescription"


class PrescriptionItem(models.Model):
    """
    用来记录一条处方内每个条目的具体信息
    """

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.DO_NOTHING,
        related_name="items",
        verbose_name="处方id",
    )
    medicine = models.ForeignKey(
        "medicine.Medicine",
        on_delete=models.DO_NOTHING,
        related_name="prescription_items",
        verbose_name="药物id",
    )
    # 如外用、温水送服等
    method = models.CharField(max_length=32, verbose_name="用法")
    # 如 3次/天等
    ratio = models.CharField(max_length=64, verbose_name="服用频率")
    # 服用时长，这个药要用多少天，为空表示此药医生可能有其他安排，应在注意事项内说明
    days = models.IntegerField(null=True, blank=True, verbose_name="服用时长")
    # 其他注意事项
    commet = models.CharField(max_length=64, verbose_name="其他")
    # 药物总数量
    count = models.IntegerField(verbose_name="药物总数量")
    # 数量单位
    count_unit = models.CharField(max_length=32, verbose_name="数量单位")
    # 每次用量，为防止如 1/3 之类的数量，使用分数来存储
    dosage = models.CharField(max_length=32, verbose_name="用量")
    # 用量单位
    dosage_unit = models.CharField(max_length=32, verbose_name="用量单位")
    # 皮试结果，为空表示没有进行皮试
    skin_test = models.CharField(
        max_length=32, null=True, blank=True, verbose_name="皮试结果"
    )

    class Meta:
        verbose_name = "处方条目"
        verbose_name_plural = "处方条目"
        db_table = "prescription_item"
