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
        read_only_fields = ["id"]


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
        validated_data.pop("name_pinyin", None)

        instance.gender = validated_data.get("gender", instance.gender)
        instance.occupation = validated_data.get(
            "occupation", instance.occupation
        )
        instance.identify_id = validated_data.get(
            "identify_id", instance.identify_id
        )
        instance.phone = validated_data.get("phone", instance.phone)
        instance.address = validated_data.get("address", instance.address)
        instance.modifier = validated_data.get("modifier", instance.modifier)

        if name:
            instance.name = name
            instance.name_pinyin = "".join(lazy_pinyin(name))
        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "profile"]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get("username"),
            password=validated_data.get("password"),
        )
        email = validated_data.get("email", None)
        if email:
            user.email = email
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.get("password", None)
        email = validated_data.get("email", None)

        if password:
            instance.set_password(password)

        if email:
            instance.email = email

        instance.save()
        return instance


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = "__all__"


class BlackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlackList
        fields = "__all__"
