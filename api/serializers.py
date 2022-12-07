from users.models import User, Product
from rest_framework import serializers


class UserRegisterationSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(
        max_length=150, write_only=True, style={"input_type": "password"}
    )
    password = serializers.CharField(
        max_length=150, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "user_type",
            "password",
            "password_2",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password_2"]:
            raise serializers.ValidationError(
                {"details": "Password fields didn't match."}
            )
        return attrs

    def save(self, **kwargs):
        validated_data = self.validated_data
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
            user_type=validated_data["user_type"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "user_type"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price")


class ProductWishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "wishlist")
