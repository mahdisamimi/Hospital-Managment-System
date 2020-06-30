from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from HospitalManagementApp import forms, models
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from HospitalManagementApp.token import account_activation_token
from django.core.mail import EmailMessage
from HospitalManagementApp.models import base_user
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm


def signup(request):

    if request.method == 'POST' and request.POST['user type'] == 'Doctor':
        form = forms.DoctorSignUpForm(request.POST)
        if form.is_valid():
            is_duplicate = base_user.objects.filter(email=form.cleaned_data.get('email')).count()
            if is_duplicate > 0:
                error_massage = "Email has been used before."
                request.session['subject'] = 'Signup'
                return render(request, 'signup.html', {'form': form, 'user_type': 'Doctor', 'error_massage': error_massage})
            form.cleaned_data['password1'] = base_user.objects.make_random_password()
            form.cleaned_data['password2'] = form.cleaned_data['password1']
            user = form.save(commit=False)
            user.is_active = False
            user.user_type = 2
            user.save()
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
            request.session['subject'] = 'Account Activation'
            request.session['massage'] = 'An email has been sent to' + form.cleaned_data.get('email') + '.\n'
            return render(request, 'massage.html')
        else:
            request.session['subject'] = 'Signup'
            return render(request, 'signup.html', {'form': form, 'user_type': 'Doctor'})
    elif request.method == 'POST' and request.POST['user type'] == 'Clerk':
        form = forms.ClerkSignUpForm(request.POST)
        if form.is_valid():
            is_duplicate = base_user.objects.filter(email=form.cleaned_data.get('email')).count()
            if is_duplicate > 0:
                error_massage = "Email has been used before."
                request.session['subject'] = 'Signup'
                return render(request, 'signup.html',
                              {'form': form, 'user_type': 'Clerk', 'error_massage': error_massage})
            form.cleaned_data['password1'] = base_user.objects.make_random_password()
            form.cleaned_data['password2'] = form.cleaned_data['password1']
            user = form.save(commit=False)
            user.is_active = False
            user.user_type = 3
            user.save()
            user.refresh_from_db()
            user.clerk.first_name = form.cleaned_data.get('first_name')
            user.clerk.last_name = form.cleaned_data.get('last_name')
            user.clerk.natural_code = form.cleaned_data.get('natural_code')
            user.clerk.phone = form.cleaned_data.get('phone')
            user.clerk.email = form.cleaned_data.get('email')
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate Your HMS Account"
            mail_massage = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                mail_subject, mail_massage, to=[form.cleaned_data.get('email')]
            )
            email.send()
            request.session['subject'] = 'Account Activation'
            request.session['massage'] = 'An email has been sent to  ' + form.cleaned_data.get('email') + '.\n'
            return render(request, 'massage.html')
        else:
            request.session['subject'] = 'Signup'
            return render(request, 'signup.html', {'form': form, 'user_type': 'Clerk'})
    elif request.method == 'GET' and 'user' in request.GET and request.GET['user'] == 'clerk':
        form = forms.ClerkSignUpForm()
        request.session['subject'] = 'Signup'
        return render(request, 'signup.html', {'form': form, 'user_type': 'Clerk'})
    elif request.method == 'GET' and 'user' in request.GET and request.GET['user'] == 'doctor':
        form = forms.DoctorSignUpForm()
        request.session['subject'] = 'Signup'
        return render(request, 'signup.html', {'form': form, 'user_type': 'Doctor'})

    else:
        request.session['subject'] = 'Signup'
        return render(request, 'signup_choice.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                request.session['subject'] = 'Login'
                request.session.update( {"massage": "Logged in successfully.\n"})
                ath_user = base_user.objects.get(username=username)
                if ath_user.user_type == 2:
                    return redirect(reverse('accounts:dashboard'))
                elif ath_user.user_type == 3:
                    return redirect(reverse('accounts:dashboard'))
                else:
                    pass #user is admin
            else:
                request.session['subject'] = 'Verify your email'
                request.session['massage'] = 'You have\'nt verified your email.please check your email and verify your registeration.'
                return render(request, 'massage.html')

        else:
            request.session['subject'] = 'Login'
            error = 'Username or Password Incorrect!'
            form = AuthenticationForm()
            return render(request, 'login.html', {'error':error, 'form':form})
    else:
        request.session['subject'] = 'Login'
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})

def account_activation_sent(request):
    request.session['subject'] = 'Login'
    form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = base_user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, base_user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token) and user.user_type == 2:
        if request.method == 'POST' :
            form = SetPasswordForm(user=user, data=request.POST)
            if form.is_valid:
                user.set_password(form.data['new_password1'])
                user.is_active = True
                user.doctor.email_confirmed = True
                user.save()
                return redirect(reverse('accounts:login'))
            else:
                request.session['subject'] = 'Login'
                form = SetPasswordForm(user=user)
                form.fields['new_password1'].lable = 'Your password'
                form.fields['new_password2'].lable = 'Your password confirmation'
                return render(request, 'password.html', {'form': form,
                                                         'first_name': user.doctor.first_name,
                                                         'uidb64':uidb64,
                                                         'token':token,
                                                         })
        else:
            request.session['subject'] = 'Login'
            form = SetPasswordForm(user=user)
            form.fields['new_password1'].lable = 'Your password'
            form.fields['new_password2'].lable = 'Your password confirmation'
            return render(request, 'password.html', {'form': form,
                                                         'first_name': user.doctor.first_name,
                                                         'uidb64':uidb64,
                                                         'token':token,
                                                         })
    elif user is not None and account_activation_token.check_token(user, token) and user.user_type == 3:
        if request.method == 'POST':
            form = SetPasswordForm(user=user)
            if form.is_valid:
                user.set_password(form.data['new_password1'])
                user.is_active = True
                user.save()
                return redirect(reverse('accounts:login'))
            else:
                request.session['subject'] = 'Login'
                form = SetPasswordForm(user=user)
                form.fields['new_password1'].lable = 'Your password'
                form.fields['new_password2'].lable = 'Your password confirmation'
                return render(request, 'password.html', {'form': form,
                                                         'first_name': user.clerk.first_name,
                                                         'uidb64':uidb64,
                                                         'token':token,
                                                         })
        else:
            request.session['subject'] = 'Login'
            form = SetPasswordForm(user=user)
            form.fields['new_password1'].lable = 'Your password'
            form.fields['new_password2'].lable = 'Your password confirmation'
            return render(request, 'password.html', {'form': form,
                                                         'first_name': user.clerk.first_name,
                                                         'uidb64':uidb64,
                                                         'token':token,
                                                         })

@login_required
def dashboard(request):
    auth_user = base_user.objects.get(username=request.user.username)
    if auth_user.user_type == 2:
        staff = auth_user.doctor
        return render(request, 'app/home/templates/index.html', {'user':staff, 'user_type':'Doctor'})
    elif auth_user.user_type == 3:
        staff = auth_user.clerk
        return render(request, 'app/home/templates/index.html', {'user':staff, 'user_type':'Clerk'})
