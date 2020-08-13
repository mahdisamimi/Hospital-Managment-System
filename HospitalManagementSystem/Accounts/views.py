from HospitalManagementApp import forms, models
from HospitalManagementApp.models import base_user
from HospitalManagementApp.models import clerk, doctor
from HospitalManagementApp.token import account_activation_token
from django.contrib.auth import login as auth_login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def is_manager(user):
    if not user.is_anonymous:
        auth_user = base_user.objects.get(username=user.username)
        if auth_user.user_type == 1:
            return True
    else:
        return False


@user_passes_test(lambda user: is_manager(user), login_url='permission denied', redirect_field_name=None)
def signup(request):
    if request.method == 'POST' and request.POST['user type'] == 'Doctor':
        form = forms.DoctorSignUpForm(request.POST)
        if form.is_valid():
            is_duplicate = base_user.objects.filter(email=form.cleaned_data.get('email')).count()
            if is_duplicate > 0:
                error_massage = "Email has been used before."
                request.session['subject'] = 'Signup'
                return render(request, 'signup.html',
                              {'form': form, 'user_type': 'Doctor', 'error_massage': error_massage})
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


@user_passes_test(lambda user: not user.is_authenticated or user.is_superuser, login_url='accounts:dashboard',
                  redirect_field_name=None)
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                request.session['subject'] = 'Login'
                request.session.update({"massage": "Logged in successfully.\n"})
                ath_user = base_user.objects.get(username=username)
                if ath_user.user_type == 2:
                    return redirect(reverse('accounts:dashboard'))
                elif ath_user.user_type == 3:
                    return redirect(reverse('accounts:dashboard'))
                elif ath_user.user_type == 1:
                    return redirect(reverse('accounts:dashboard'))
            else:
                request.session['subject'] = 'Verify your email'
                request.session[
                    'massage'] = 'You have\'nt verified your email.please check your email and verify your registeration.'
                return render(request, 'massage.html')

        else:
            request.session['subject'] = 'Login'
            error = 'Username or Password Incorrect!'
            form = AuthenticationForm()
            return render(request, 'login.html', {'error': error, 'form': form})
    else:
        request.session['subject'] = 'Login'
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def account_activation_sent(request):
    request.session['subject'] = 'Login'
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = base_user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, base_user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token) and user.user_type == 2:
        if request.method == 'POST':
            form = SetPasswordForm(user=user, data=request.POST)
            if form.is_valid:
                user.set_password(form.data['new_password1'])
                user.is_active = True
                user.doctor.email_confirmed = True
                user.save()
                return redirect(reverse('accounts:login'))
            else:
                request.session['subject'] = 'Avtivate'
                form = SetPasswordForm(user=user)
                form.fields['new_password1'].lable = 'Your password'
                form.fields['new_password2'].lable = 'Your password confirmation'
                return render(request, 'password.html', {'form': form,
                                                         'first_name': user.doctor.first_name,
                                                         'uidb64': uidb64,
                                                         'token': token,
                                                         })
        else:
            if user.is_active == False:
                request.session['subject'] = 'Avtivate'
                form = SetPasswordForm(user=user)
                form.fields['new_password1'].lable = 'Your password'
                form.fields['new_password2'].lable = 'Your password confirmation'
                return render(request, 'password.html', {'form': form,
                                                         'first_name': user.doctor.first_name,
                                                         'uidb64': uidb64,
                                                         'token': token,
                                                         })
            else:
                request.session['subject'] = 'Account Password'
                request.session[
                    'massage'] = 'Sorry, This page is not available for you anymore.'
                return render(request, 'massage.html')

    elif user is not None and account_activation_token.check_token(user, token) and user.user_type == 3:
        if request.method == 'POST':
            form = SetPasswordForm(user=user, data=request.POST)
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
                                                         'uidb64': uidb64,
                                                         'token': token,
                                                         })
        else:
            if user.is_active == False:
                request.session['subject'] = 'Login'
                form = SetPasswordForm(user=user)
                form.fields['new_password1'].lable = 'Your password'
                form.fields['new_password2'].lable = 'Your password confirmation'
                return render(request, 'password.html', {'form': form,
                                                         'first_name': user.clerk.first_name,
                                                         'uidb64': uidb64,
                                                         'token': token,
                                                         })
            else:
                request.session['subject'] = 'Account Password'
                request.session[
                    'massage'] = 'Sorry, This page is not available for you anymore.'
                return render(request, 'massage.html')

    elif user is not None and account_activation_token.check_token(user, token) and user.user_type == 1:
        if request.method == 'POST':
            form = SetPasswordForm(user=user, data=request.POST)
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
                                                         'first_name': user.manager.first_name,
                                                         'uidb64': uidb64,
                                                         'token': token,
                                                         })
        else:
            if user.is_active == False:
                request.session['subject'] = 'Login'
                form = SetPasswordForm(user=user)
                form.fields['new_password1'].lable = 'Your password'
                form.fields['new_password2'].lable = 'Your password confirmation'
                return render(request, 'password.html', {'form': form,
                                                         'first_name': user.manager.first_name,
                                                         'uidb64': uidb64,
                                                         'token': token,
                                                         })
            else:
                request.session['subject'] = 'Account Password'
                request.session[
                    'massage'] = 'Sorry, This page is not available for you anymore.'
                return render(request, 'massage.html')

    else:
        request.session['subject'] = 'Wrong Address!'
        request.session[
            'massage'] = 'Sorry, This page is not available for you.'
        return render(request, 'massage.html')


@login_required
def dashboard(request):
    auth_user = base_user.objects.get(username=request.user.username)
    if auth_user.user_type == 2:
        staff = auth_user.doctor

        return render(request, 'app/home/templates/index.html', {'user': staff, 'user_type': 'Doctor'})
    elif auth_user.user_type == 3:
        staff = auth_user.clerk

        return render(request, 'app/home/templates/index.html', {'user': staff, 'user_type': 'Clerk'})
    elif auth_user.user_type == 1:
        staff = auth_user.manager

        return render(request, 'app/home/templates/index.html', {'user': staff, 'user_type': 'Manager'})


# This view handles showing user information while in dashboard.
@login_required
def usri(request):
    auth_user = base_user.objects.get(username=request.user.username)
    if auth_user.user_type == 2:
        staff = auth_user.doctor

        return render(request, 'app/home/templates/usri.html', {'user': staff, 'user_type': 'Doctor'})
    elif auth_user.user_type == 3:
        staff = auth_user.clerk

        return render(request, 'app/home/templates/usri.html', {'user': staff, 'user_type': 'Clerk'})
    elif auth_user.user_type == 1:
        staff = auth_user.manager

        return render(request, 'app/home/templates/usri.html', {'user': staff, 'user_type': 'Manager'})


@user_passes_test(lambda user: user.is_superuser, login_url='permission denied', redirect_field_name=None)
def manager_signup(request):
    if request.method == 'POST':
        form = forms.ManagerSignUpForm(request.POST)
        if form.is_valid():
            is_duplicate = base_user.objects.filter(email=form.cleaned_data.get('email')).count()
            if is_duplicate > 0:
                error_massage = "Email has been used before."
                request.session['subject'] = 'Signup'
                return render(request, 'signup_manager.html', {'form': form, 'error_massage': error_massage})
            form.cleaned_data['password1'] = base_user.objects.make_random_password()
            form.cleaned_data['password2'] = form.cleaned_data['password1']
            user = form.save(commit=False)
            user.is_active = False
            user.user_type = 1
            user.save()
            user.refresh_from_db()
            user.manager.first_name = form.cleaned_data.get('first_name')
            user.manager.last_name = form.cleaned_data.get('last_name')
            user.manager.natural_code = form.cleaned_data.get('natural_code')
            user.manager.phone = form.cleaned_data.get('phone')
            user.manager.email = form.cleaned_data.get('email')
            user.manager.hospital_name = form.cleaned_data.get('hospital_name')
            user.manager.hospital_id = form.cleaned_data.get('hospital_id')
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
            request.session['massage'] = 'An email has been sent to' + form.cleaned_data.get('email') + '.\n'
            return render(request, 'massage.html')
        else:
            request.session['subject'] = 'Signup A Manager'
            return render(request, 'signup_manager.html', {'form': form, })
    else:
        form = forms.ManagerSignUpForm()
        request.session['subject'] = 'Signup A Manager'
        return render(request, 'signup_manager.html', {'form': form, })


def permission_denied(request):
    return render(request, 'permission-denied.html')


def change_password(request):
    try:
        auth_user = base_user.objects.get(username=request.user.username)
    except (TypeError, ValueError, OverflowError, base_user.DoesNotExist):
        auth_user = None
    if auth_user is None:
        return render(request, 'permission-denied.html')
    if request.method == 'POST':
        form = PasswordChangeForm(user=auth_user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:dashboard'))
        else:
            request.session['subject'] = 'Avtivate'
            return render(request, 'change password.html', {'form': form,
                                                            })
    else:
        request.session['subject'] = 'Avtivate'
        form = PasswordChangeForm(user=auth_user)
        return render(request, 'change password.html', {'form': form,
                                                        })


def modify(request):
    try:
        auth_user = base_user.objects.get(username=request.user.username)
    except (TypeError, ValueError, OverflowError, base_user.DoesNotExist):
        auth_user = None
    if auth_user is None:
        return render(request, 'permission-denied.html')
    if auth_user.user_type == 1:  # manager
        if request.method == 'POST':
            form = forms.ManagerEditProfileForm(data=request.POST, instance=auth_user.manager)
            if form.is_valid():
                form.save()
                return redirect(reverse('accounts:dashboard'))
            else:
                request.session['subject'] = 'Edit Profile'
                return render(request, 'signup.html', {'form': form, 'user': auth_user.manager
                                                       })
        else:
            form = forms.ManagerEditProfileForm(instance=auth_user.manager)
            request.session['subject'] = 'Edit Profile'
            return render(request, 'signup.html', {'form': form, 'user': auth_user.manager
                                                   })
    elif auth_user.user_type == 2:  # doctor
        if request.method == 'POST':
            form = forms.DoctorEditProfileForm(data=request.POST, instance=auth_user.doctor)
            if form.is_valid():
                form.save()
                return redirect(reverse('accounts:dashboard'))
            else:
                request.session['subject'] = 'Edit Profile'
                return render(request, 'signup.html', {'form': form, 'user': auth_user.doctor
                                                       })
        else:
            form = forms.DoctorEditProfileForm(instance=auth_user.doctor)
            request.session['subject'] = 'Edit Profile'
            return render(request, 'signup.html', {'form': form, 'user': auth_user.doctor
                                                   })
    elif auth_user.user_type == 3:  # clerk
        if request.method == 'POST':
            form = forms.ClerkEditProfileForm(data=request.POST, instance=auth_user.clerk)
            if form.is_valid():
                form.save()
                auth_user.save()
                return redirect(reverse('accounts:dashboard'))
            else:
                request.session['subject'] = 'Edit Profile'
                return render(request, 'signup.html', {'form': form, 'user': auth_user.clerk
                                                       })
        else:
            form = forms.ClerkEditProfileForm(instance=auth_user.clerk)
            request.session['subject'] = 'Edit Profile'
            return render(request, 'app/home/templates/auth-signup.html', {'form': form, 'user': auth_user.clerk
                                                                           })


def rezerv(request):
    # return render(request,'rezerv.html')
    if request.method == 'POST':
        # form = forms.DoctorSignUpForm(request.POST)
        form = forms.ReservesForm(request.POST)
        if form.is_valid():
            # is_duplicate = User.objects.filter(email=form.cleaned_data.get('email')).count()
            # if is_duplicate > 0:
            #     error_massage = "Email has been used before"
            #     return render(request, 'rezerv.html', {'form': form, 'error_massage': error_massage})
            user = form.save()
            user.is_active = False
            user.refresh_from_db()
            user.reserve.doctor_id = form.cleaned_data.get('doctor_id')
            user.reserve.reserve_time = form.cleaned_data.get('reserve_time')
            user.reserve.natural_code = form.cleaned_data.get('natural_code')
            user.reserve.clerk_id = form.cleaned_data.get('clerk_id')
            user.save()

            request.session['subject'] = 'Account Activation'
            request.session['massage'] = 'An email has been sent to' + form.cleaned_data.get('email') + '.\n'
            return render(request, 'massage.html')
    else:
        form = forms.ReservesForm(request.POST)
        request.session['subject'] = 'Signup'
    return render(request, 'rezerv2.html', {'form': form})


# def create_rezerv(request):
#     new_rezerv = reserve(doctor_id=request.POST.get('doctor_id'))
#     new_rezerv.save()
#     return redirect('/accounts/rezerv_list/')
#

def rezerv_list(request):
    rezervs = reserve.objects.all()
    return render(request, 'rezerv_list2.html', {'rezerv': rezervs})


def delete_rezerv(request, id=None):
    rezervs = reserve.objects.get(id=id)
    rezervs.delete()
    return redirect('/accounts/rezerv_list/')


def update_rezerv(request, id):
    rezervs = reserve.objects.get(id=id)
    if request.method == 'POST':
        # form = forms.DoctorSignUpForm(request.POST)
        form = forms.ReservesForm(request.POST)
        if form.is_valid():
            # is_duplicate = User.objects.filter(email=form.cleaned_data.get('email')).count()
            # if is_duplicate > 0:
            #     error_massage = "Email has been used before"
            #     return render(request, 'rezerv.html', {'form': form, 'error_massage': error_massage})
            user = form.save()
            user.is_active = False
            user.refresh_from_db()
            user.reserve.doctor_id = form.cleaned_data.get('doctor_id')
            user.reserve.reserve_time = form.cleaned_data.get('reserve_time')
            user.reserve.natural_code = form.cleaned_data.get('natural_code')
            user.reserve.clerk_id = form.cleaned_data.get('clerk_id')
            user.save()

            request.session['subject'] = 'Account Activation'
            request.session['massage'] = 'An email has been sent to' + form.cleaned_data.get('email') + '.\n'
            return render(request, 'massage.html')
    else:
        form = forms.ReservesForm(request.POST)
        request.session['subject'] = 'Signup'
    # return render(request, 'rezerv.html', )
    form2 = ReservesForm(initial={'doctor_id': rezervs.doctor_id, 'reserve_time': rezervs.reserve_time,
                                  'natural_code': rezervs.natural_code, 'clerk_id': rezervs.clerk_id})
    # form2=form.fields['natural_code'].initial = reverse.natural_code
    return render(request, 'rezerv_update2.html', {'form': form2, 'id': id})


def updating(request):
    id = request.POST['id']
    rezervs = reserve.objects.get(id=id)
    rezervs.doctor_id = doctor.objects.get(id=request.POST['doctor_id'])
    rezervs.natural_code = request.POST['natural_code']
    rezervs.reserve_time = free_time.objects.get(id=request.POST['rezerv_time'])
    rezervs.save()
    return redirect('/accounts/rezerv_list/')
