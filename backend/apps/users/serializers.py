"""
User serializers.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer for read operations."""
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "avatar",
            "bio",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    """User serializer for registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        attrs.pop("password_confirm")
        return attrs

    def create(self, validated_data):
        from apps.users.services import user_create
        return user_create(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    """User serializer for updates."""
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "bio", "avatar"]

    def update(self, instance, validated_data):
        from apps.users.services import user_update
        return user_update(user=instance, **validated_data)


class UserMeSerializer(serializers.ModelSerializer):
    """Extended user serializer for authenticated user."""
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "avatar",
            "bio",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "username", "email", "created_at", "updated_at"]
