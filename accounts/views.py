from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from .models import Account

# verification mail
from RECTECH import settings
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name    =form.cleaned_data['first_name']
            last_name     =form.cleaned_data['last_name']
            email         =form.cleaned_data['email']
            phone_number  =form.cleaned_data['phone_number']
            password      =form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number= phone_number
            user.save()
            messages.success(request, 'Thank you for registering with us . We have sent an verification email to your email address please verify it')
            current_site = get_current_site(request)
            mail_subject = 'Welcome to RECTECH'
            message = render_to_string('accounts/welcome_email.html',{
               'user':user,
            })
            to_email = email
            send_mail = EmailMessage(mail_subject,message, to =[to_email])
            send_mail.send()
            # User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
              'user':user,
              'domain': current_site,
              'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
              'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(mail_subject,message, to =[to_email])
            send_mail.send()
            return redirect('/accounts/login/?command=verification&email='+email)


    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, 'You are now logged in')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out ')
    return redirect('login')


def activate(request, uidb64, token):
    # return HttpResponse('ok')
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation ! Your account is activated')
        return redirect('login')
    else:
        messages.error(rewuest, 'Invalid activation link')
        return redirect('register')



def profile(request):

    return render(request, 'accounts/profile.html')

def thanks(request):
    return render(request, 'accounts/thanks.html')
