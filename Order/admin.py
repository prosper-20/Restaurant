from django.contrib import admin
from .models import Order, OrderItem, Item, BillingAddress, Payment, Coupon

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    ]
    


admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Item)
admin.site.register(BillingAddress)
admin.site.register(Coupon)
admin.site.register(Payment)
