from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Customer

@receiver(post_save, sender=Customer)
def customer_update(sender, instance, created, **kwargs):
    if created:
        print(f"New customer created: {instance.full_name} (ID: {instance.id})")
    else:
        print(f"Сustomer data updated: {instance.full_name} (ID: {instance.id})")

@receiver(post_delete, sender=Customer)
def customer_deletion(sender, instance, **kwargs):
    print(f"Customer deleted: {instance.full_name} (ID: {instance.id})")
