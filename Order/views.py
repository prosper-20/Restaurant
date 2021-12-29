from django.db import models
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, reverse, render, get_object_or_404
from stripe.api_resources import order
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.views.generic import View
from .forms import CheckoutForm, CouponForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY

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
            return redirect("item_list")
        


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
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                "form": form,
                "couponform": CouponForm(),
                "DISPLAY_COUPON_FORM": True,
                'order': order
            }
            return render(self.request, "Order/checkout-page.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")
        
        
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get("street_address")
                apartment_address = form.cleaned_data.get("apartment_address")
                country = form.cleaned_data.get("country")
                zip = form.cleaned_data.get("zip")
                # TO BE WORKED ON LATER
                # same_shipping_addres = form.cleaned_data.get("same_shipping_addres")
                # save_info = form.cleaned_data.get("save_info")
                payment_option = form.cleaned_data.get("payment_option")
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country= country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                if payment_option == "S":
                    return redirect('payment', payment_option='stripe')
                elif payment_option == "P":
                    return redirect('payment', payment_option='paypal')
                else:
                    # add redirect to the selected payment option 
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("order_summary")
        


class PaymentView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        # order
        order =  order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                "order": order,
                "DISPLAY_COUPON_FORM": False
            }
            return render(self.request, 'Order/payment.html', context)
        else:
            messages.warning(self.request, "You have not added a billing address")
            return redirect("checkout")


    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount=int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount, #Cents
                currency='usd',
                source="tok_mastercard"
            )
            #CREATE A PAYMENT
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign payment to Order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was successful")
            return redirect("item_list")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("item_list")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate Limit Error")
            return redirect("item_list")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Invalid Request Error")
            return redirect("item_list")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Oops! Authentication Error")
            return redirect("item_list")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Connection couldn't be established")
            return redirect("item_list")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(self.request, "Something went wrong. Pls try again")
            return redirect("item_list")
        except Exception as e:
            # Send an email
            messages.warning(self.request, "A serious error occured, we are on it.")
            return redirect("item_list")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get("code")
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("checkout")

            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout")
    



        

        
        