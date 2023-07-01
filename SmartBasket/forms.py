from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class CustomLoginForm(forms.Form):
    username = forms.CharField(label='Корисничко име')
    password = forms.CharField(widget=forms.PasswordInput, label='Лозинка')

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'


class CustomerRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=100, label='Адреса')
    phone_number = forms.CharField(max_length=100, label='Телефонски број')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'address', 'phone_number']
        labels = {'username': 'Корисничко име', 'first_name': 'Име', 'last_name': 'Презиме', 'email': 'E-mail'}

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Лозинка'
        self.fields['password2'].label = 'Потврди лозинка'
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class SalesmanRegistrationForm(UserCreationForm):
    market = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-select'}), label='Маркет')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'market']
        labels = {'username': 'Корисничко име',
                  'first_name': 'Име',
                  'last_name': 'Презиме',
                  'email': 'E-mail'}

    def __init__(self, *args, **kwargs):
        super(SalesmanRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Лозинка'
        self.fields['password2'].label = 'Потврди лозинка'
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
        labels = {'username': 'Корисничко име', 'first_name': 'Име', 'last_name': 'Презиме', 'email': 'E-mail'}

    def __init__(self, *args, **kwargs):
        super(DeliverymanRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Лозинка'
        self.fields['password2'].label = 'Потврди лозинка'
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
        labels = {'date_of_pickup': 'Датум и време на подигнување', 'first_name': 'Име', 'last_name': 'Презиме',
                  'phone_number': 'Телефонски број'}

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
        labels = {'date_of_delivery': 'Датум и време на достава', 'first_name': 'Име', 'last_name': 'Презиме',
                  'phone_number': 'Телефонски број', 'address': 'Адреса', 'payment_option': 'Начин на плаќање'}

    def __init__(self, *args, **kwargs):
        super(DeliveryOrderForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'
            if v.name == 'payment_option':
                v.field.widget.attrs['class'] = 'form-select'


class PaymentForm(forms.Form):
    card = forms.CharField(max_length=19, min_length=19, required=True,
                           widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}))
    cvv = forms.CharField(max_length=3, min_length=3, required=True,
                          widget=forms.TextInput(attrs={'placeholder': 'CVV'}), label='CVV')
    expiry_data = forms.CharField(max_length=5, min_length=5, required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []
        labels = {'name': 'Име', 'description': 'Опис', 'price': 'Цена', 'category': 'Категорија', 'image': 'Слика',
                  'quantity': 'Количина'}

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs['class'] = 'form-control'
            if v.name == 'category':
                v.field.widget.attrs['class'] = 'form-select'
