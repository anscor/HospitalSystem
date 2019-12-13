from .models import *

from rest_framework import serializers
from pypinyin import lazy_pinyin


class GroupProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProfile
        exclude = ["id"]


class GroupSerializer(serializers.ModelSerializer):
    profile = GroupProfileSerializer(required=False)

    class Meta:
        model = Group
        fields = ["id", "name", "profile"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ["id"]
        read_only_fields = ["name_pinyin"]

    def create(self, validated_data):
        name = validated_data.get("name")
        name_pinyin = "".join(lazy_pinyin(name))
        validated_data["name_pinyin"] = name_pinyin
        profile = UserProfile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        name = validated_data.pop("name", None)
        if name:
            instance.name = name
            instance.name_pinyin = "".join(lazy_pinyin(name))
        instance.save()

        UserProfile.objects.update(instance, **validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "profile"]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["id"]

    # def update(self, instance, validated_data):

    #     password = validated_data.pop('password', None)
    #     if password:
    #         instance.set_password(password)
    #     instance.sava()
    #     User.objects.update(instance, **validated_data)
    #     return instance
