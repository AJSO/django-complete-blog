from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils import *

from .forms import SignUpForm
from .tokens import account_activation_token

def SignUp_View(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        # user can't login until link confirmed
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        email_subject = 'Activate Your Account'
        # load a template like get_template() 
        # and calls its render() method immediately.
        messages.success(request, 'Form submission successful')
        #message = render_to_string('accounts/activation_request.html', {
        #    'user': user,
        #    'domain': current_site.domain,
        #    'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
        #     method will generate a hash value with user related data
        #   'token': account_activation_token.make_token(user),
        # })
        message = render_to_string('accounts/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
        #user.email_user(subject, message)
        #return redirect('activation_sent')
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        #return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
        return redirect('activation_sent')

    else:
        # messages.success(request, 'Form submission successful')
        messages.error(request, 'Oops!! Something went wrong..')
        form = SignUpForm()
        context = {
            'form': form,
        }
    return render(request, 'accounts/signUp.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        # login(request, user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
    else:
        return render(request, 'accounts/activation_invalid.html')

def activation_sent_view(request):
    return render(request, 'accounts/activation_sent.html')

def home_view(request):
    return render(request, 'accounts/home.html')

def profile(request):
    return render(request, 'accounts/profile.html')

#=============================Alternative to signup_view=========================
#def usersignup(request):
#    if request.method == 'POST':
#        form = UserSignUpForm(request.POST)
#        if form.is_valid():
#            user = form.save(commit=False)
#            user.is_active = False
#            user.save()
#            current_site = get_current_site(request)
#            email_subject = 'Activate Your Account'
#            message = render_to_string('activate_account.html', {
#                'user': user,
#                'domain': current_site.domain,
#                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
#                'token': account_activation_token.make_token(user),
#            })
#            to_email = form.cleaned_data.get('email')
#            email = EmailMessage(email_subject, message, to=[to_email])
#            email.send()
#            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
#    else:
#        form = UserSignUpForm()
#    return render(request, 'signup.html', {'form': form})
#def activate_account(request, uidb64, token):
#    try:
#        uid = force_bytes(urlsafe_base64_decode(uidb64))
#        user = User.objects.get(pk=uid)
#    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#        user = None
#    if user is not None and account_activation_token.check_token(user, token):
#        user.is_active = True
#        user.save()
#        login(request, user)
#        return HttpResponse('Your account has been activate successfully')
#    else:
#        return HttpResponse('Activation link is invalid!')
#    
def sigin_view(request):
    pass
