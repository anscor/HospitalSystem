from django.db import models
from django.contrib.auth.models import User, Group

from reservation.models import Reservation
from finance.models import PayRecord


class WaitQueue(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="wait_queues",
        verbose_name="病人id",
    )

    department = models.ForeignKey(
        Group,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="wait_queues",
        verbose_name="科室id",
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="doctor_wait_queues",
        verbose_name="医生id",
    )

    pay = models.OneToOneField(
        PayRecord,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="wait_queue",
        verbose_name="缴费id",
    )

    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="wait_queue",
        verbose_name="预约id",
    )

    joined_time = models.DateTimeField(
        auto_now_add=True, verbose_name="开始排队时间"
    )

    def __lt__(self, other):
        # 有预约优先
        if self.reservation and not other.reservation:
            return True
        elif not self.reservation and other.reservation:
            return False
        # 都有或都没有预约时，比较到达时间，到达时间早的优先
        else:
            return self.joined_time < other.joined_time

    def __eq__(self, other):
        return self.patient == other.patient

    class Meta:
        managed = False
        db_table = "wait_queue"
