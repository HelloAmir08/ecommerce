from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Product, ProductSpecification, Image, Comment
admin.site.register(User)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'discounted_price', 'stock', 'rating')
    list_filter = ('category', 'stock', 'rating')
    search_fields = ('name', 'description')
    inlines = [ImageInline, ProductSpecificationInline]

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'key', 'value')
    search_fields = ('product__name', 'key', 'value')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'full_name', 'email', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('full_name', 'email', 'review')
