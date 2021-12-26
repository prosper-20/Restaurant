from django.db import models
from django.contrib import messages
from django.shortcuts import redirect, reverse, render, get_object_or_404
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.views.generic import View


class HomeView(ListView):
    model = Item
    context_object_name = "items"
    template_name = 'Order/today_home_page.html'
    paginate_by = 10


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'Order/order_summary.html')



class ItemDetailView(DetailView):
    model = Item
    template_name = 'Order/product-page.html'

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the orderitem is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect('product', slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart")
            return redirect('product', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect('product', slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
         ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the orderitem is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('product', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)
    return redirect('product', slug=slug)




def product(request):
    return render(request, "Order/product-page.html")
