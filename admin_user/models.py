from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создание обычного пользователя"""
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона", blank=True, null=True)
    activation_code_created_at = models.DateTimeField(null=True, blank=True)  # Время генерации кода
    reset_code = models.CharField(max_length=100, blank=True, null=True)  # Поле для кода сброса
    activation_code = models.CharField(max_length=4, blank=True, null=True)  # Активационный код
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")  # Поле для определения роли администратора

    USERNAME_FIELD = 'email'  # Логин будет через email
    REQUIRED_FIELDS = []  # Не нужно указывать email, так как это USERNAME_FIELD

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email