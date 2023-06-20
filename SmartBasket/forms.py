from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'


class CustomerRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class SalesmanRegistrationForm(UserCreationForm):
    market = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'market']

    def __init__(self, *args, **kwargs):
        super(SalesmanRegistrationForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            if v.name != 'market':
                v.field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class DeliverymanRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(DeliverymanRegistrationForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class PickUpOrderForm(forms.ModelForm):
    class Meta:
        model = PickUpOrder
        exclude = ['market', 'picked_up']

    def __init__(self, *args, **kwargs):
        super(PickUpOrderForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'
            if v.name == 'date_of_pickup':
                v.field.widget = forms.DateInput(attrs={'type': 'datetime-local'})
                v.field.widget.attrs['class'] = 'form-control'


class DeliveryOrderForm(forms.ModelForm):
    class Meta:
        model = DeliveryOrder
        exclude = ['market', 'delivered', 'deliveryman']

    def __init__(self, *args, **kwargs):
        super(DeliveryOrderForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'
