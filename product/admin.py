from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Image, ProductSpecification, Comment

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'get_discounted_price', 'stock', 'rating', 'created_at')
    list_filter = ('stock', 'category', 'rating', 'created_at')
    search_fields = ('name', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ImageInline, ProductSpecificationInline]

    def view_image(self, obj):
        if obj.get_image_url:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;"/>', obj.get_image_url)
        return "No Image"
    view_image.short_description = "Preview"

    @admin.display(description="Discounted Price")
    def get_discounted_price(self, obj):
        return f"{obj.discounted_price:.2f}"

    @admin.action(description="Activate selected products")
    def make_active(self, request, queryset):
        queryset.update(stock=True)




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'full_name', 'email', 'rating', 'created_at')
    search_fields = ('full_name', 'product__name')
