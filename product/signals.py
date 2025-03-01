from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from .models import Product
from user.models import User
import os
import json
from config.settings import BASE_DIR


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        email_of_users = [user.email for user in users]
        if email_of_users:
            send_mail(
                'New product created',
                f"{instance.name} created",
                'amirjontoirov03@gmail.com',
                email_of_users,
            )


@receiver(pre_delete, sender=Product)
def product_pre_delete(sender, instance, **kwargs):
    product_data = {
        'id': instance.id,
        'name': instance.name,
        'description': instance.description,
        'price': float(instance.price),
        'discount': instance.discount,
        'category': instance.category.name if instance.category else None,
        'quantity': instance.quantity,
        'stock': instance.stock,
        'rating': instance.rating,
        'created_at': str(instance.created_at),
        'updated_at': str(instance.updated_at),
        'product_specification': [
            {'key': spec.key, 'value': spec.value} for spec in instance.specifications.all()
        ]
    }

    file_path = os.path.join(BASE_DIR, 'product_data/pre_delete_product_data', f'product_{instance.id}_data.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(product_data, f, indent=3, ensure_ascii=False)


@receiver(post_delete, sender=Product)
def product_post_delete(sender, instance, **kwargs):
    users = User.objects.all()
    email_of_users = [user.email for user in users]

    if email_of_users:
        send_mail(
            'Product deleted',
            f"{instance.name} deleted",
            'amirjontoirov03@gmail.com',
            email_of_users,
        )


@receiver(pre_save, sender=Product)
def product_update(sender, instance, **kwargs):
    if instance.id:
        product_old_data = {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'price': float(instance.price),
            'discount': instance.discount,
            'category': instance.category.name if instance.category else None,
            'quantity': instance.quantity,
            'stock': instance.stock,
            'rating': instance.rating,
            'created_at': str(instance.created_at),
            'updated_at': str(instance.updated_at),
            'product_specification': [
                {'key': spec.key, 'value': spec.value} for spec in instance.specifications.all()
            ]
        }

        file_path = os.path.join(BASE_DIR, 'product_data/product_pre_save_data', f'product_{instance.id}_data.json')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(product_old_data, f, indent=3, ensure_ascii=False)
