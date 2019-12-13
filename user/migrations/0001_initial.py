# Generated by Django 3.0 on 2019-12-12 23:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Occupation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="职业名")),
            ],
            options={
                "verbose_name": "职业列表",
                "verbose_name_plural": "职业列表",
                "db_table": "occupation",
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("age", models.IntegerField(verbose_name="年龄")),
                ("name", models.CharField(max_length=64, verbose_name="用户名称")),
                (
                    "name_pinyin",
                    models.CharField(max_length=255, verbose_name="用户名拼音"),
                ),
                (
                    "gender",
                    models.IntegerField(
                        choices=[(0, "女"), (1, "男")], verbose_name="性别"
                    ),
                ),
                (
                    "identify_id",
                    models.CharField(max_length=18, verbose_name="身份证号"),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        verbose_name="联系电话",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="住址"
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="创建时间"
                    ),
                ),
                (
                    "modify_time",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="修改时间"
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_user_profiles",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建者id",
                    ),
                ),
                (
                    "modifier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="modified_user_profiles",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="修改者id",
                    ),
                ),
                (
                    "occupation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="users",
                        to="user.Occupation",
                        verbose_name="职业id",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户id",
                    ),
                ),
            ],
            options={
                "verbose_name": "用户信息",
                "verbose_name_plural": "用户信息",
                "db_table": "user_profile",
            },
        ),
        migrations.CreateModel(
            name="UserLogRecord",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ip",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="IP地址"
                    ),
                ),
                (
                    "operation",
                    models.IntegerField(
                        choices=[(0, "登录"), (1, "登出")], verbose_name="操作类型"
                    ),
                ),
                (
                    "operate_time",
                    models.DateTimeField(auto_now=True, verbose_name="操作时间"),
                ),
                (
                    "operator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="operations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="操作者id",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="logs",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户id",
                    ),
                ),
            ],
            options={
                "verbose_name": "用户登录相关日志记录",
                "verbose_name_plural": "用户登录相关日志记录",
                "db_table": "user_log_record",
            },
        ),
        migrations.CreateModel(
            name="GroupProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="位置"
                    ),
                ),
                (
                    "contact_phone",
                    models.CharField(
                        blank=True,
                        max_length=12,
                        null=True,
                        verbose_name="联系电话",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="创建时间"
                    ),
                ),
                (
                    "modify_time",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="修改时间"
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_group_profiles",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建者id",
                    ),
                ),
                (
                    "group",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to="auth.Group",
                        verbose_name="组id",
                    ),
                ),
                (
                    "modifier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="modified_group_profiles",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="修改者id",
                    ),
                ),
            ],
            options={
                "verbose_name": "组信息",
                "verbose_name_plural": "组信息",
                "db_table": "group_profile",
            },
        ),
        migrations.CreateModel(
            name="BlackList",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "join_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="加入时间"
                    ),
                ),
                (
                    "is_delete",
                    models.BooleanField(
                        choices=[(0, "否"), (1, "是")],
                        default=0,
                        verbose_name="是否从黑名单移除",
                    ),
                ),
                (
                    "reason",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        null=True,
                        verbose_name="加入黑名单原因",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_black_lists",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建者id",
                    ),
                ),
                (
                    "patient",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="is_black",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="病人id",
                    ),
                ),
            ],
            options={
                "verbose_name": "黑名单",
                "verbose_name_plural": "黑名单",
                "db_table": "black_list",
            },
        ),
    ]