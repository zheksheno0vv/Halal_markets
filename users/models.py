from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Укажи свой реальный домен
    frontend_url = "https://example.com"  # Заменить на адрес твоего сайта или фронтенда

    # Генерация полного URL сброса пароля
    reset_url = "{}{}?token={}".format(
        frontend_url,
        reverse('password_reset:reset-password-request'),  # Django-обработчик, можно заменить
        reset_password_token.key
    )

    # Отправка письма
    send_mail(
        subject="Password Reset for Some Website",  # Тема
        message=f"Use the following link to reset your password:\n{reset_url}",  # Текст
        from_email="noreply@example.com",  # Отправитель
        recipient_list=[reset_password_token.user.email],  # Получатель
        fail_silently=False,
    )




class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()

