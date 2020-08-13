from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User , Group
from HospitalManagementApp.models import doctor,clerk,free_time
from.models import base_user ,reserve
from django.forms import ModelForm
import datetime
class ReservesForm(ModelForm):
    class Meta:
        model = reserve
        fields = ['doctor_id', 'reserve_time', 'natural_code', 'clerk_id', ]

    doctor_id = forms.ModelChoiceField(queryset=doctor.objects.all())
    reserve_time = forms.ModelChoiceField(queryset=free_time.objects.all())
    natural_code = forms.IntegerField()
    clerk_id = forms.ModelChoiceField(queryset=clerk.objects.all())
    # !!ADVANCED!! hospital = models.ForeignKey(hospital, on_delete=models.CASCADE)



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