from datetime import timedelta
from time import timezone
from django.core.mail import BadHeaderError
from django.contrib.auth.password_validation import validate_password
from rest_framework import status, generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from .serializers import *
import random
import string
import re
from django.utils import timezone
import logging
from .models import CustomUser
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
import random
import string
import logging
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
import logging
logger = logging.getLogger(__name__)

User = get_user_model()
def generate_activation_code():
    """Генерирует случайный код активации, состоящий только из цифр, длиной 4 символа."""
    return ''.join(random.choices(string.digits, k=4))

class AdminRegistrationView(generics.CreateAPIView):
    """View для регистрации нового администратора."""
    serializer_class = AdminRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        logger.debug(f"Registration request data: {request.data}")
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return Response({
                'response': False,
                'message': _('Ошибка валидации')
            }, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')

        try:
            user = serializer.save()
            user.is_active = False  # Сначала устанавливаем неактивным
            user.set_password(password)  # Устанавливаем пароль
            user.save()

            # Генерация и установка кода активации
            activation_code = generate_activation_code()
            user.activation_code = activation_code  # Сохраняем код активации # Сохраняем время создания кода активации
            user.save()

            # Формирование сообщения на русском языке
            message_ru = (
                f"<h1>{_('Здравствуйте')}, {user.email}!</h1>"
                f"<p>{_('Поздравляем Вас с успешной регистрацией на сайте')} {settings.BASE_URL}</p>"
                f"<p>{_('Ваш код активации')}: {activation_code}</p>"
                f"<p>{_('С наилучшими пожеланиями')},<br>{_('Команда')} {settings.BASE_URL}</p>"
            )

            # Отправка письма
            email_subject = _('Активация вашего аккаунта')

            try:
                send_mail(
                    email_subject,
                    '',  # Пустое текстовое сообщение, т.к. используем html_message
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                    html_message=message_ru,
                )
                logger.debug(f"Activation email sent to {user.email}")

                # Активируем администратора после отправки письма
                user.is_active = True  # Теперь активируем пользователя
                user.save()

            except Exception as e:
                logger.error(f"Error sending activation email: {str(e)}")
                return Response({
                    'response': False,
                    'message': _('Не удалось отправить письмо с кодом активации.')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'response': True,
                'message': _(
                    'Пользователь успешно зарегистрирован. Проверьте вашу электронную почту для получения кода активации.')
            }, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            logger.error(f"IntegrityError: {str(e)}")
            if 'email' in str(e):
                return Response({
                    'response': False,
                    'message': _('Такой email уже зарегистрирован.')
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'response': False,
                'message': _('Не удалось зарегистрировать пользователя.')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Функция для активации администратора
def activate_admin(email):
    try:
        user = User.objects.get(email=email)
        user.is_active = True  # Активируем пользователя
        user.save()
        print(f"Пользователь {email} успешно активирован.")
    except User.DoesNotExist:
        print(f"Пользователь с email {email} не найден.")

class ActivationAPIView(generics.GenericAPIView):
    serializer_class = ActivationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Сериализатор невалиден: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        activation_code = serializer.validated_data.get('activation_code')
        try:
            user = get_object_or_404(CustomUser, activation_code=activation_code)

            # Проверка срока действия кода (1 час)
            if user.activation_code_created_at and timezone.now() > user.activation_code_created_at + timedelta(hours=1):
                return Response({
                    'response': False,
                    'message': _('Срок действия кода активации истек.')
                }, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.activation_code = ''
            user.activation_code_created_at = None
            user.save()

            return Response({
                'response': True,
                'message': _('Ваш аккаунт успешно активирован.')
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Ошибка активации: {str(e)}")
            return Response({
                'response': False,
                'message': _('Ошибка активации.')
            }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.CreateAPIView):
    """Аутентификация пользователя."""
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')

        if user is None:
            return Response({
                'response': False,
                'message': _('Неверный логин или пароль.')
            }, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'response': True,
            'token': token.key
        }, status=status.HTTP_200_OK)


def generate_reset_code(length=4):
    """Генерация кода сброса из случайных цифр."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
class ResetPasswordView(generics.GenericAPIView):
    """Запрос на сброс пароля."""
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
            reset_code = generate_reset_code()  # Генерация кода сброса пароля
            user.reset_code = reset_code
            user.save()

            message = (
                f"Здравствуйте, {user.email}!\n\n"
                f"{_('Ваш код активации')}: {reset_code}\n\n"
                f"Ваш код для восстановления пароля: {reset_code}\n\n"
                f"С наилучшими пожеланиями,\nКоманда {settings.BASE_URL}"
            )
            send_mail(
                _('Восстановление пароля'),
                '',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message,
            )

            return Response({
                'response': True,
                'message': _('Письмо с инструкциями по восстановлению пароля было отправлено на ваш email.')
            })

        except CustomUser.DoesNotExist:
            return Response({
                'response': False,
                'message': _('Пользователь с этим адресом электронной почты не найден.')
            }, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordVerifyView(generics.GenericAPIView):
    """Подтверждение кода сброса пароля."""
    serializer_class = ResetPasswordVerifySerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_code = serializer.validated_data['reset_code']

        try:
            user = CustomUser.objects.get(reset_code=reset_code)
            user.reset_code = ''  # Очищаем код сброса после подтверждения
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'response': True,
                'message': _('Код успешно подтвержден.'),
                'token': token.key
            }, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            logger.error(f"User with reset_code {reset_code} does not exist.")
            return Response({
                'response': False,
                'message': _('Неверный код для сброса пароля.')
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error in ResetPasswordVerifyView: {str(e)}")
            return Response({
                'response': False,
                'message': _('Произошла ошибка при сбросе пароля.')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResendActivationCodeView(generics.GenericAPIView):
    """Повторная отправка кода активации на email."""
    serializer_class = ResendActivationCodeSerializer
    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
            # Генерация нового кода активации
            activation_code = generate_activation_code()
            user.activation_code = activation_code
            user.activation_code_created_at = timezone.now()
            user.save()

            message = (
                f"Здравствуйте, {user.email}!\n\n"
                f"<p>{_('Ваш новый код активации')}: {activation_code}</p>"
                f"<p>{_('С наилучшими пожеланиями')},<br>{_('Команда')} {settings.BASE_URL}</p>"
            )

            try:
                send_mail(
                    _('Активация вашего аккаунта'),
                    '',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                    html_message=message,
                )
            except BadHeaderError:
                return Response({
                    'response': False,
                    'message': _('Ошибка при отправке письма. Попробуйте еще раз позже.')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'response': True,
                'message': _('Новый код активации был отправлен на ваш email.')
            })

        except CustomUser.DoesNotExist:
            return Response({
                'response': False,
                'message': _('Пользователь с этим адресом электронной почты не найден.')
            }, status=status.HTTP_404_NOT_FOUND)

class ResenActivationCodeView(generics.GenericAPIView):
    """Повторная отправка кода активации на email."""
    serializer_class = ResendActivationCodeSerializer
    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
            # Генерация нового кода восстановления пароля
            reset_code = generate_activation_code()  # Изменено на reset_code
            user.reset_code = reset_code
            user.reset_code_created_at = timezone.now()
            user.save()

            message = (
                f"Здравствуйте, {user.email}!\n\n"
                f"<p>{_('Ваш код для восстановления пароля')}: {reset_code}</p>"  # Сообщение для восстановления пароля
                f"<p>{_('С наилучшими пожеланиями')},<br>{_('Команда')} {settings.BASE_URL}</p>"
            )

            try:
                send_mail(
                    _('Восстановление пароля'),
                    '',  # Пустое тело, так как мы используем html_message
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                    html_message=message,
                )

            except BadHeaderError:
                return Response({
                    'response': False,
                    'message': _('Ошибка при отправке письма. Попробуйте еще раз позже.')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'response': True,
                'message': _('Новый код для восстановления пароля был отправлен на ваш email.')
            })

        except CustomUser.DoesNotExist:
            return Response({
                'response': False,
                'message': _('Пользователь с этим адресом электронной почты не найден.')
            }, status=status.HTTP_404_NOT_FOUND)

class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # Проверка старого пароля
            if not user.check_password(old_password):
                return Response({'error': 'Неверный старый пароль.'}, status=status.HTTP_400_BAD_REQUEST)

            # Установка нового пароля
            user.set_password(new_password)
            user.save()

            return Response({'success': 'Пароль успешно изменен.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)