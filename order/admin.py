from django.contrib import admin

from .models import ProductCategory, Product, Order, OrderItem, Stock, StockItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    raw_id_fields = ['product']


class StockItemInline(admin.TabularInline):
    model = StockItem
    extra = 0


@admin.register(ProductCategory)
class ProductCategory(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'phonenumber', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated', 'phonenumber', 'address']
    inlines = [OrderItemInline]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address', 'contact_phone']
    list_display = ['name', 'address', 'contact_phone']
    inlines = [StockItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    inlines = [StockItemInline]
