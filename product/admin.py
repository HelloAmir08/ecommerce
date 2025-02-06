from django.contrib import admin

from product.models import Product, Category, Image, ProductSpecification, Comment

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(ProductSpecification)
admin.site.register(Comment)