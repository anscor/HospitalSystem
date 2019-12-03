from django.db import models
from django.contrib.auth.models import User, Group


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户id')

    name = models.CharField(max_length=64, verbose_name='用户名称')
    name_pinyin = models.CharField(max_length=255, verbose_name='用户名拼音')

    GENDER = (
        (0, '女'),
        (1, '男')
    )
    gender = models.IntegerField(choices=GENDER, verbose_name='性别')
    identify_id = models.CharField(max_length=18, verbose_name='身份证号')

    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                related_name='created_user_profiles', verbose_name='创建者id')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modifier = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True,
                                 blank=True, related_name='modified_user_profiles', verbose_name='修改者id')
    modify_time = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
        db_table = 'user_profile'


class GroupProfile(models.Model):

    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, related_name='profile', verbose_name='组id')

    location = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='位置')
    contact_phone = models.CharField(
        max_length=12, null=True, blank=True, verbose_name='联系电话')

    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                related_name='created_group_profiles', verbose_name='创建者id')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modifier = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True,
                                 blank=True, related_name='modified_group_profiles', verbose_name='修改者id')
    modify_time = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '组信息'
        verbose_name_plural = '组信息'
        db_table = 'group_profile'
