from django.db import models
from django.contrib.auth.models import User, Group

IS_NOT = ((0, "否"), (1, "是"))


class Occupation(models.Model):
    """
    此表为职业名与id的一个对应列表
    """

    name = models.CharField(max_length=255, verbose_name="职业名")

    class Meta:
        verbose_name = "职业列表"
        verbose_name_plural = "职业列表"
        db_table = "occupation"


class UserProfile(models.Model):
    GENDER = ((0, "女"), (1, "男"))

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="用户id",
    )
    occupation = models.ForeignKey(
        Occupation,
        on_delete=models.DO_NOTHING,
        related_name="users",
        verbose_name="职业id",
    )

    name = models.CharField(max_length=64, verbose_name="用户名称")
    name_pinyin = models.CharField(max_length=255, verbose_name="用户名拼音")
    gender = models.IntegerField(choices=GENDER, verbose_name="性别")
    identify_id = models.CharField(max_length=18, verbose_name="身份证号")
    phone = models.CharField(
        max_length=13, null=True, blank=True, verbose_name="联系电话"
    )
    address = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="住址"
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_user_profiles",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modifier = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="modified_user_profiles",
        verbose_name="修改者id",
    )
    modify_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="修改时间"
    )

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"
        db_table = "user_profile"


class GroupProfile(models.Model):

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="组id",
    )

    parent_group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children_groups",
        verbose_name="父组id",
    )

    location = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="位置"
    )
    contact_phone = models.CharField(
        max_length=12, null=True, blank=True, verbose_name="联系电话"
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_group_profiles",
        verbose_name="创建者id",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modifier = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="modified_group_profiles",
        verbose_name="修改者id",
    )
    modify_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="修改时间"
    )

    class Meta:
        verbose_name = "组信息"
        verbose_name_plural = "组信息"
        db_table = "group_profile"


class BlackList(models.Model):
    patient = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        related_name="is_black",
        verbose_name="病人id",
    )

    join_time = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")
    is_delete = models.BooleanField(
        choices=IS_NOT, verbose_name="是否从黑名单移除", default=0
    )
    reason = models.CharField(
        max_length=64, null=True, blank=True, verbose_name="加入黑名单原因"
    )

    # 一般为系统默认添加，但有时候可能会由工作人员人为设置
    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_black_lists",
        verbose_name="创建者id",
    )

    class Meta:
        verbose_name = "黑名单"
        verbose_name_plural = "黑名单"
        db_table = "black_list"
