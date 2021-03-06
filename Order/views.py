from django.db import models
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.expressions import Ref
from django.shortcuts import redirect, reverse, render, get_object_or_404
from stripe.api_resources import order
from Order.models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile, ItemImage
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.views.generic import View
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import stripe
from django.conf import settings
import random
import string 
# from sendgrid import SendGridAPIClient
from django.contrib.auth.models import User

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from sendgrid.helpers.mail import SandBoxMode, MailSettings


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def is_valid_form(values):
    valid = True
    for field in values:
        if field == "":
            valid = False
    return valid

stripe.api_key = settings.STRIPE_SECRET_KEY

class HomeView(ListView):
    model = Item
    context_object_name = "items"
    template_name = 'Order/today_home_page.html'
    paginate_by = 100


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
    photos = ItemImage.objects.all()
    # context = {"photos": photos}
    template_name = 'Order/product-page.html'
    extra_context={'photos': ItemImage.objects.all()}

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
            # return redirect('product', slug=slug)
            return redirect('order_summary')
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



class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):  # You added pk to it
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                "form": form,
                "couponform": CouponForm(),
                "order": order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address': shipping_address_qs[0]})

            # FOR THE BILLING ADDRESS
            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update({'default_billing_address': billing_address_qs[0]})

            return render(self.request, "Order/checkout-page.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")
       
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)        # YOU added Pk
            if form.is_valid():

                use_deafult_shipping = form.cleaned_data.get("use_default_shipping")
                if use_deafult_shipping:
                    print('Using the default shipping address')
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, "No default shipping address available")
                        return redirect("checkout")

                else:
                    print("User is etrering a new shipping address ")
                    shipping_address1 = form.cleaned_data.get("shipping_address")
                    shipping_address2 = form.cleaned_data.get("shipping_address2")
                    shipping_country = form.cleaned_data.get("shipping_country")
                    shipping_zip = form.cleaned_data.get("shipping_zip")

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type="S"
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(self.request, "Please fill in the required shipping address fields")

                use_deafult_billing = form.cleaned_data.get("use_default_shipping")
                same_billing_address = form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = "B"
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_deafult_billing:
                    print('Using the default billing address')
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request, "No default billing address available")
                        return redirect("checkout")

                else:
                    print("User is etrering a new billing address ")
                    billing_address1 = form.cleaned_data.get("billing_address")
                    billing_address2 = form.cleaned_data.get("billing_address2")
                    billing_country = form.cleaned_data.get("billing_country")
                    billing_zip = form.cleaned_data.get("billing_zip")

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type="B"
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get("payment_option")
                # ADD REDIRECT TO PAYMENT OPTION

                if payment_option == 'S':
                    return redirect("payment", payment_option="stripe")
                elif payment_option == "P":
                    return redirect("payment", payment_option="paypal")
                else:
                    messages.warning(self.request, "Invalid Payment Option Selected")
                    return redirect("checkout")

            messages.warning(self.request, "Failed Checkout")
            return redirect("checkout")

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order_summary")
        


class PaymentView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        # order
        order =  order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                "order": order,
                "DISPLAY_COUPON_FORM": False,
                'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLISHABLE_KEY
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    context.update[{
                        'card': card_list[0]
                    }]
            return render(self.request, 'Order/payment.html', context)
        else:
            messages.warning(self.request, "You have not added a billing address")
            return redirect("checkout")


    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        # You added this
        post_mail = order.user.email
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        # You still added this
        new_order = Order.objects.filter(id=self.request.user.id).last()

        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            # This is for sending the mail, You switched the template from confirmation-copy.html to order_on_its_way
            html_template = 'restaurant/order_on_its_way_2.html'
            my_dict = {"order": order, "new_order": new_order}
            html_message = render_to_string(html_template, context=my_dict)
            subject = "Order Confirmation"
            email_from = settings.EMAIL_HOST_USER
            # recipient_list = ["babatundemubaraq1650@gmail.com"]
            recipient_list = [post_mail]
            message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
            message.content_subtype = "html"
            message.send()
            
            # for order_item in order.items.all:
            #     order_item.get_total_item_price
            #     order_item.item.title

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)
    

        try:

            if use_default or save:
                # charge the customer because we cannot charge the token more than once
                charge = stripe.Charge.create(
                    amount=amount,  # cents
                    currency="usd",
                    customer=userprofile.stripe_customer_id
                )
            else:
                # charge once off on the token
                charge = stripe.Charge.create(
                    amount=amount,  # cents
                    currency="usd",
                    source=token
                )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()


            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()

            
            messages.success(self.request, "Your order was successful!")
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

        messages.warning(self.request, "Invalid data received")
        return redirect("payment")


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
    


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            "form": form
        }
        return render(self.request, 'request_refund.html', context)


    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get("message")
            email = form.cleaned_data.get('email')
            # Edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request has been received.")
                return redirect('item_list')

            except ObjectDoesNotExist():
                messages.info(self.request, "This order doesn't exist")
                return redirect('request_refund')



def snacks_view(request):
    items = Item.objects.filter(category="S").all().order_by('-id')
    context = {
        "items": items,
    }
    return render(request, "Order/snacks.html", context)

def appetizers_view(request):
    items = Item.objects.filter(category="A").all().order_by('-id')
    context = {
        "items": items,
    }
    return render(request, "Order/appetizer.html", context)

def maincourse_view(request):
    items = Item.objects.filter(category="MC").all().order_by('-id')
    context = {
        "items": items,
    }
    return render(request, "Order/main_course.html", context)

def desserts_view(request):
    items = Item.objects.filter(category="E").all().order_by('-id')
    context = {
        "items": items,
    }
    return render(request, "Order/desserts.html", context)

def dentist_view(request):
    return render(request, "Order/dentist.html")


class reservation_view(ListView):
    model = Item
    context_object_name = "items"
    template_name = 'Order/reservation.html'
    paginate_by = 100

def appointment(request):
    if request.method == "POST":
        your_name = request.POST['your-name']
        your_phone = request.POST['your-phone']
        your_email = request.POST['your-email']
        your_date = request.POST['your-date']
        your_schedule = request.POST['your-schedule']
        your_time = request.POST['your-time']
        your_message = request.POST['your-message']

        html_template = "Order/beefree-b48ua1rg62h.html"
        my_dict = {
            "your_name": your_name,
            "your_phone": your_phone,
            "your_email": your_email,
            "your_date": your_date,
            "your_schedule": your_schedule,
            "your_time": your_time,
            "your_message": your_message,
        }
        html_message = render_to_string(html_template, context= my_dict)
        subject = "Reservation Confirmation"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [your_email]
        message = EmailMessage(subject, html_message,
                                email_from, recipient_list)
        message.content_subtype = "html"
        message.send()
        # send_mail(
        #     "Appointment Confirmation",
        #     "God is good",
        #     "edwardprosper001@gmail.com",
        #     ['your_email']
        # )
    
        messages.success(request, f"Hi {your_name}, your reservation has been placed. Kindly Click On the Link in your mail to confrim your reservation.")
        return render(request, 'Order/appointment.html', {
        "your_name": your_name,
        "your_phone": your_phone,
        "your_email": your_email,
        "your_date": your_date,
        "your_schedule": your_schedule,
        "your_time": your_time,
        "your_message": your_message,
        
    })

    else:
        return render(request, 'Order/reservation.html')



class NewConfirmationView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "object": order,
            }
            return render(self.request, "restaurant/confirmation-copy.html", context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("item_list")



def search_posts(request):
    if request.method == "POST":
        searched = request.POST['searched']
        # This returns the results of the user's search
        items = Item.objects.filter(title__contains=searched)
        return render(request, "order/new_search_posts.html", {'searched': searched, 'items': items})
    else:
        return render(request, "order/new_search_posts.html")







        

        
        