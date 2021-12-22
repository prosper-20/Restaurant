from django.db import models
from django.shortcuts import redirect, reverse, render, get_object_or_404
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone

class HomeView(ListView):
    model = Item
    context_object_name = "items"
    template_name = 'Order/new_home_page.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'Order/product-page.html'

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.create(item=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the orderitem is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect('product', slug=slug)



def product(request):
    return render(request, "Order/product-page.html")
