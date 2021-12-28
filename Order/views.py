from django.db import models
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, reverse, render, get_object_or_404
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.views.generic import View
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(ListView):
    model = Item
    context_object_name = "items"
    template_name = 'Order/today_home_page.html'
    paginate_by = 10

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "object": order,
            }
            return render(self.request, 'Order/order_summary.html', context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")
        


class ItemDetailView(DetailView):
    model = Item
    template_name = 'Order/product-page.html'

@login_required
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

@login_required
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
            return redirect('order_summary')
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)
    return redirect('product', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
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
            # This is so the order will be delted once the item no. is zero
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated ")
            return redirect('order_summary')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('product', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)
    return redirect('product', slug=slug)




def product(request):
    return render(request, "Order/product-page.html")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm
        context = {
            "form": form
        }
        return render(self.request, "Order/checkout-page.html", context)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            street_address = form.cleaned_data.get("street_address")
            apartment_address = form.cleaned_data.get("apartment_address")
            country = form.cleaned_data.get("country")
            zip = form.cleaned_data.get("zip")
            same_billing_address = form.cleaned_data.get("same_billing_address")
            save_info = form.cleaned_data.get("save_info")
            payment_option = form.cleaned_data.get("payment_option")
            
            return redirect('checkout')
        messages.warning(self.request, "Failed Checout")
        return redirect('checkout')
