from django.db import models
from django.contrib.auth.models import User, Group


class Occupation(models.Model):
    '''
    此表为职业名与id的一个对应列表
    '''
    name = models.CharField(max_length=255, verbose_name='职业名')

    class Meta:
        verbose_name = '职业列表'
        verbose_name_plural = '职业列表'
        db_table = 'occupation'


class UserProfile(models.Model):
    GENDER = (
        (0, '女'),
        (1, '男')
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户id')
    occupation = models.ForeignKey(
        Occupation, on_delete=models.DO_NOTHING, related_name='users', verbose_name='职业id')

    age = models.IntegerField(verbose_name='年龄')
    name = models.CharField(max_length=64, verbose_name='用户名称')
    name_pinyin = models.CharField(max_length=255, verbose_name='用户名拼音')
    gender = models.IntegerField(choices=GENDER, verbose_name='性别')
    identify_id = models.CharField(max_length=18, verbose_name='身份证号')
    phone = models.CharField(max_length=13, null=True,
                             blank=True, verbose_name='联系电话')
    address = models.CharField(
        max_length=256, null=True, blank=True, verbose_name='住址')

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


class UserLogRecord(models.Model):
    # 被操作者
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='logs', verbose_name='用户id')

    ip = models.GenericIPAddressField(
        null=True, blank=True, verbose_name='IP地址')

    OPERATION = (
        (0, '登录'),
        (1, '登出')
    )
    operation = models.IntegerField(choices=OPERATION, verbose_name='操作类型')

    # 操作者，一般而言与user相同，但有可能是管理员操作（user被动下线等）
    operator = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='operations', verbose_name='操作者id')
    operate_time = models.DateTimeField(auto_now=True, verbose_name='操作时间')

    class Meta:
        verbose_name = '用户登录相关日志记录'
        verbose_name_plural = '用户登录相关日志记录'
        db_table = 'user_log_record'
