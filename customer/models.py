
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Customer(BaseModel):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField(region="UZ")
    address= models.CharField(max_length=100)
    image = models.ImageField(upload_to='customer_image', null=True, blank=True, default='customer_image/default.jpg')

    @property
    def get_absolute_url(self):
        if self.image:
            return self.image.url
        return '/media/customer_image/default.jpg'

    def __str__(self):
        return self.full_name

