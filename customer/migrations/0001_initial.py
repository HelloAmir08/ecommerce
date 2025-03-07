# Generated by Django 5.1.5 on 2025-02-10 17:50

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='UZ')),
                ('address', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, default='customer_image/default.jpg', null=True, upload_to='customer_image')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
