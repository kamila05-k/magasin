from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser

class AdminRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate(self, data):
        """Проверка, что пароли совпадают"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        """Создание пользователя с подтверждением пароля"""
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Неверный логин или пароль.")
        return {'user': user}

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordVerifySerializer(serializers.Serializer):
    reset_code = serializers.CharField(max_length=100)

class ActivationCodeSerializer(serializers.Serializer):
    activation_code = serializers.CharField(max_length=4)

class ResendActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
