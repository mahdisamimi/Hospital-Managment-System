from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DoctorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required =True)
    last_name = forms.CharField(max_length=255, required =True)
    natural_code = forms.IntegerField(required =True)
    msn = forms.IntegerField(required =True)
    phone = forms.IntegerField(required =True)
    email = forms.CharField(max_length=40, required =True, help_text = "Enter valid Email Address. You will be asked for Verification.")
    # !!ADVANCED!! hospital = models.ForeignKey(hospital, on_delete=models.CASCADE)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'natural_code', 'msn', 'phone', 'email', )
