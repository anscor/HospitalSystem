from django.db import models
from django.contrib.auth.models import User

PAY_METHOD = ((0, "现金"), (1, "银联"), (2, "支付宝"), (3, "微信"))


class PayRecord(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="paid_records",
        verbose_name="病人id",
    )

    receive = models.FloatField(verbose_name="收款金额")
    refund = models.FloatField(verbose_name="找零")
    method = models.IntegerField(choices=0, verbose_name="收款方式", default=0)

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_pay_records",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "缴费记录"
        verbose_name_plural = "缴费记录"
        db_table = "pay_record"


class PayType(models.Model):
    name = models.CharField(max_length=256, verbose_name="类型名")
    price = models.FloatField(verbose_name="价格")

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_pay_types",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modifier = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="modified_pay_types",
        verbose_name="修改者id",
    )
    modify_time = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="修改时间"
    )

    class Meta:
        verbose_name = "缴费类型"
        verbose_name_plural = "缴费类型"
        db_table = "pay_type"


class PayItem(models.Model):
    record = models.ForeignKey(
        PayRecord,
        on_delete=models.DO_NOTHING,
        related_name="items",
        verbose_name="缴费单id",
    )
    pay_type = models.ForeignKey(
        PayType,
        on_delete=models.DO_NOTHING,
        related_name="items",
        verbose_name="缴费项目id",
    )
    # 数量、次数
    count = models.IntegerField(verbose_name="数量")

    class Meta:
        verbose_name = "缴费项目"
        verbose_name_plural = "缴费项目"
        db_table = "pay_item"


class RefundRecord(models.Model):
    item = models.ForeignKey(
        PayItem,
        on_delete=models.DO_NOTHING,
        related_name="refunds",
        verbose_name="项目id",
    )

    method = models.IntegerField(
        choices=PAY_METHOD, verbose_name="退款方式", default=0
    )
    refund = models.FloatField(verbose_name="退款金额")
    reason = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="退款原因"
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_refund_records",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "退款记录"
        verbose_name_plural = "退款记录"
        db_table = "refund_record"


class AuditRecord(models.Model):

    AUDIT_RESULT = ((0, "通过"), (1, "未通过"))

    result = models.IntegerField(
        choices=AUDIT_RESULT, verbose_name="审核结果", default=0
    )
    # 如未通过填写原因
    commet = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="备注"
    )

    applicant = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="applied_records",
        verbose_name="申请者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")
    auditor = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="audited_records",
        verbose_name="审核者id",
    )
    audit_time = models.DateTimeField(auto_now_add=True, verbose_name="审核时间")

    class Meta:
        verbose_name = "结算审核记录"
        verbose_name_plural = "结算审核记录"
        db_table = "audit_record"


class AuditItem(models.Model):
    audit = models.ForeignKey(
        AuditRecord,
        on_delete=models.DO_NOTHING,
        related_name="items",
        verbose_name="审核id",
    )
    receive = models.ForeignKey(
        PayRecord,
        on_delete=models.DO_NOTHING,
        related_name="audit_items",
        verbose_name="收款条目id",
    )
    refund = models.ForeignKey(
        RefundRecord,
        on_delete=models.DO_NOTHING,
        related_name="audit_items",
        verbose_name="退款条目",
    )

    class Meta:
        verbose_name = "结算条目"
        verbose_name_plural = "结算条目"
        db_table = "audit_item"
