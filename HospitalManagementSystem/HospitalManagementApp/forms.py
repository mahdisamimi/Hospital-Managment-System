from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from HospitalManagementApp.models import doctor
from.models import base_user



class DoctorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required =True)
    last_name = forms.CharField(max_length=255, required =True)
    natural_code = forms.IntegerField(required =True)
    msn = forms.IntegerField(required =True)
    phone = forms.IntegerField(required =True)
    email = forms.CharField(max_length=40, required =True, help_text = "Enter valid Email Address. You will be asked for Verification.")
    # !!ADVANCED!! hospital = models.ForeignKey(hospital, on_delete=models.CASCADE)
    class Meta:
        model = base_user
        fields = ('username', 'first_name', 'last_name', 'natural_code', 'msn', 'phone', 'email', )
    def __init__(self, *args, **kargs):
        super(DoctorSignUpForm, self).__init__(*args, **kargs)
        self.fields.pop('password1')
        self.fields.pop('password2')

class ClerkSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required =True)
    last_name = forms.CharField(max_length=255, required =True)
    natural_code = forms.IntegerField(required =True)
    phone = forms.IntegerField(required =True)
    email = forms.CharField(max_length=40, required =True, help_text = "Enter valid Email Address. You will be asked for Verification.")
    # !!ADVANCED!! hospital = models.ForeignKey(hospital, on_delete=models.CASCADE)
    class Meta:
        model = base_user
        fields = ('username', 'first_name', 'last_name', 'natural_code', 'phone', 'email', )
    def __init__(self, *args, **kargs):
        super(ClerkSignUpForm, self).__init__(*args, **kargs)
        self.fields.pop('password1')
        self.fields.pop('password2')

class ManagerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    natural_code = forms.IntegerField(required=True)
    phone = forms.IntegerField(required=True)
    email = forms.CharField(max_length=40, required=True,
                            help_text="Enter valid Email Address. You will be asked for Verification.")
    hospital_name = forms.CharField(max_length=255, required=True)
    hospital_id = forms.IntegerField(required=True)

    class Meta:
        model = base_user
        fields = ('username', 'first_name', 'last_name', 'natural_code', 'phone', 'email', 'hospital_name', 'hospital_id', )

    def __init__(self, *args, **kargs):
        super(ManagerSignUpForm, self).__init__(*args, **kargs)
        self.fields.pop('password1')
        self.fields.pop('password2')