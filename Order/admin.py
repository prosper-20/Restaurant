from django.contrib import admin
from .models import Order, OrderItem, Item, Address, Payment, Coupon, Refund, UserProfile, Category, ItemImage

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = "Update orders to refund granted"


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'Being_delivered',
                    'Received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]

    list_display_links = ['user',
                          'shipping_address',
                          'billing_address',
                          'payment',
                          'coupon'
                        ]

    list_filter = ['ordered',
                    'Being_delivered',
                    'Received',
                    'refund_requested',
                    'refund_granted',
                ]
    search_fields = ['user__username',
                     'ref_code'
                    ]

    actions=[make_refund_accepted]
    

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default',
    ]

    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']

admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
# admin.site.register(Item)
admin.site.register(Address, AddressAdmin)
admin.site.register(Coupon)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(UserProfile)
admin.site.register(Category)
# admin.site.register(ItemImage)


class ItemImageAdmin(admin.StackedInline):
    model = ItemImage

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemImageAdmin]

    class Meta:
        model = Item

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    pass