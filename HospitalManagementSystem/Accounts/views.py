from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from HospitalManagementApp import forms, models
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from HospitalManagementApp.token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User




def signup(request):
    if request.method == 'POST':
        form = forms.DoctorSignUpForm(request.POST)
        if form.is_valid():
            is_duplicate = User.objects.filter(email=form.cleaned_data.get('email')).count()
            if is_duplicate > 0:
                error_massage = "Email has been used before"
                return render(request, 'signup.html', {'form': form, 'error_massage': error_massage})
            user = form.save()
            user.is_active = False
            user.refresh_from_db()
            user.doctor.first_name = form.cleaned_data.get('first_name')
            user.doctor.last_name = form.cleaned_data.get('last_name')
            user.doctor.natural_code = form.cleaned_data.get('natural_code')
            user.doctor.msn = form.cleaned_data.get('msn')
            user.doctor.phone = form.cleaned_data.get('phone')
            user.doctor.email = form.cleaned_data.get('email')
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate Your HMS Account"
            mail_massage = render_to_string('account_activation_email.html', {
                'user' : user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                mail_subject, mail_massage, to=[form.cleaned_data.get('email')]
            )
            email.send()
            return redirect('account_activation_sent')
    else:
        form = forms.DoctorSignUpForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    pass

def account_activation_sent(request):
    render('base_layout.html', {})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.doctor.email_confirmed = True
        user.save()
        login(user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')