from django.db import models
from django.contrib.auth.models import User, Group

IS_NOT = (
    (0, '否'),
    (1, '是')
)


class ReservationTime(models.Model):
    '''
    预约时间段定义，记录一个开始时间与结束时间
    一般两时间间隔为30分钟，且时间记录有效位仅到分，秒、毫秒等无效
    '''
    start = models.TimeField(verbose_name='开始时间')
    end = models.TimeField(verbose_name='结束时间')
    patient_num = models.IntegerField(verbose_name='此时间段内最大可接待患者数')

    class Meta:
        verbose_name = '预约时间段'
        verbose_name_plural = '预约时间段'
        db_table = 'reservation_time'


class Reservation(models.Model):
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                related_name='reservations', verbose_name='病人id')
    department = models.ForeignKey(
        Group, on_delete=models.DO_NOTHING, related_name='reservations', verbose_name='科室id')

    # 哪一天去看病
    date = models.DateField(verbose_name='预约日期')
    # 这一天哪个时间段
    time = models.ForeignKey(ReservationTime, on_delete=models.DO_NOTHING,
                             related_name='reservations', verbose_name='预约时间段')

    is_cancel = models.BooleanField(
        choices=IS_NOT, verbose_name='是否取消', default=0)

    # 下面两个字段相互关联，如果是专家号才会有医生id，如果不是则医生id为空
    is_expert = models.BooleanField(
        choices=IS_NOT, verbose_name='是否为专家号', default=0)
    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True,
                               blank=True, related_name='be_reservations', verbose_name='医生id')

    class Meta:
        verbose_name = '预约记录'
        verbose_name_plural = '预约记录'
        db_table = 'reservation'


class Visit(models.Model):

    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='visits', verbose_name='医生id')

    date = models.DateField(verbose_name='坐诊日期')

    # 此处时间间隔通常为半天或一天
    start = models.TimeField(verbose_name='坐诊开始时间')
    end = models.TimeField(verbose_name='坐诊结束时间')

    patient_num = models.IntegerField(verbose_name='最大可接待患者数')

    class Meta:
        verbose_name = '专家坐诊时间'
        verbose_name_plural = '专家坐诊时间'
        db_table = 'visit'

