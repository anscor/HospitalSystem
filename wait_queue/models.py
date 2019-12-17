from django.db import models
from django.contrib.auth.models import User, Group

from reservation.models import Reservation


class WaitQueue(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="wait_queues",
        verbose_name="病人id",
    )

    department = models.ForeignKey(
        Group,
        on_delete=models.DO_NOTHING,
        related_name="wait_patients",
        verbose_name="科室id",
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="wait_patients",
        verbose_name="医生id",
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
        # 没有预约时，比较到达时间，到达时间早的优先
        elif not self.reservation and not other.reservation:
            return self.joined_time < other.joined_time

        # 都有预约
        # 专家号优先
        if self.reservation.is_expert and not other.reservation.is_expert:
            return True
        elif not self.reservation.is_expert and other.reservation.is_expert:
            return False
        # 都不是或者都是专家号时，比较到达时间，到达时间早的优先
        else:
            return self.joined_time < other.joined_time

    class Meta:
        managed = False
        db_table = "wait_queue"
