from django.urls import path
from .views import *
urlpatterns = [ # Включаем маршруты из роутера
    path('register/', AdminRegistrationView.as_view(), name='admin_register'),
    path('activate/', ActivationAPIView.as_view(), name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password-verify/', ResetPasswordVerifyView.as_view(), name='reset_password_verify'),
    path('resend-activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),
    path('resen-password-verify-code/', ResenActivationCodeView.as_view(), name='resend_activation_code'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

]