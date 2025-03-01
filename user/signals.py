from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from .models import User
import os
import json
from config.settings import BASE_DIR


@receiver(post_save, sender=User)
def user_registered_signal(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        email_of_users = [user.email for user in users]

        if email_of_users:
            send_mail(
                'New User Registered',
                f'{instance.get_full_name()} has registered',
                'amirjontoirov03@gmail.com',
                email_of_users,
            )
        print('User Registered')


@receiver(pre_delete, sender=User)
def user_pre_delete_signal(sender, instance, **kwargs):
    user_data = {
        'id': instance.id,
        'full_name': instance.get_full_name(),
        'email': instance.email,
        'username': instance.username,
        'date_joined': str(instance.date_joined),
        'last_login': str(instance.last_login),
    }

    file_path = os.path.join(BASE_DIR, 'user_data/pre_delete_user_data', f'user_{instance.id}_data.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, indent=3, ensure_ascii=False)


@receiver(post_delete, sender=User)
def user_deleted_signal(sender, instance, **kwargs):
    users = User.objects.all()
    email_of_users = [user.email for user in users]

    if email_of_users:
        send_mail(
            'User Deleted',
            f'{instance.get_full_name()} has been deleted',
            'amirjontoirov03@gmail.com',
            email_of_users,
        )


@receiver(pre_save, sender=User)
def user_pre_save_data(sender, instance, **kwargs):
    user_data = {
        'id': instance.id,
        'full_name': instance.get_full_name(),
        'email': instance.email,
        'username': instance.username,
        'date_joined': str(instance.date_joined),
        'last_login': str(instance.last_login),
    }

    file_path = os.path.join(BASE_DIR, 'user_data/pre_save_user_data', f'user_{instance.id}_data.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, indent=3, ensure_ascii=False)