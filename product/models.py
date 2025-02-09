from django.db import models
from decimal import Decimal

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(BaseModel):
    class RatingChoice(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    stock = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(choices=RatingChoice.choices, default=RatingChoice.ZERO.value)


    @property
    def get_image_url(self):
        image = self.images.first()
        if image and image.image:
            return image.image.url
        return "/static/default-image.jpg"
    @property
    def discounted_price(self):
        if self.discount > 0:
            new_price = Decimal(self.price) * Decimal((1 - self.discount / 100))
        else:
            new_price = self.price
        return new_price.quantize(Decimal('0.01'))

    def __str__(self):
        return self.name
class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"


class Image(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_image/', null=True, blank=True)

from django.db import models

class Comment(BaseModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.full_name} - {self.rating} stars'






