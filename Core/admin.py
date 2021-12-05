from django.contrib import admin
from .models import OrderModel, MenuItem, Category


class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_paid']

admin.site.register(OrderModel, OrderAdmin)
admin.site.register(MenuItem)
admin.site.register(Category)
