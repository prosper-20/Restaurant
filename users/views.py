from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from sendgrid.helpers.mail import SandBoxMode, MailSettings



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hi {username}, your account has been created successfully! Sign In below")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})

def register1(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Huff ,Username already exist')
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Come On, Email was already Taken !')
            return redirect("register")
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            mydict = {'username': username}
            mail_settings = MailSettings()
            mail_settings.sandbox_mode = SandBoxMode(False)
            user.save()
            html_template = 'users/index.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = "P's Diner"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            messages.success(request, f'Account created for {username}! You can now login')
            return redirect("login")
    else:
        return render(request, 'users/register1.html')



def profile(request):
    return render(request, 'users/profile.html')


def profile_edit(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, 'users/profile_edit.html', context)



