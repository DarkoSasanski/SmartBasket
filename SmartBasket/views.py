from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import *
from .models import *


# Create your views here.

def index(request):
    return render(request, 'index.html')


def login_customer(request):
    form = CustomLoginForm()
    err = 'None'
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if Customer.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('/index')
        err = 'Invalid username or password'
    return render(request, 'login_customer.html', {'form': form, 'error': err})


def login_salesman(request):
    form = CustomLoginForm()
    err = 'None'
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                if Salesman.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('/index')
        err = 'Invalid username or password'
    return render(request, 'login_salesman.html', {'form': form, 'error': err})


def login_deliveryman(request):
    form = CustomLoginForm()
    err = 'None'
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                if Deliveryman.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('/index')
        err = 'Invalid username or password'
    return render(request, 'login_deliveryman.html', {'form': form, 'error': err})


def register_customer(request):
    form = CustomerRegistrationForm()
    err = 'None'
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = Customer(
                user=user,
                address=form.data['address'],
                phone_number=form.data['phone_number'],
            )
            customer.save()
            return redirect('/login-cust')
        err = 'Invalid input'
    return render(request, 'register_customer.html', {'form': form, 'error': err})


def register_salesman(request):
    form = SalesmanRegistrationForm()
    markets = Market.objects.all()
    form.fields['market'].choices = [(market.id, market.name) for market in markets]
    err = 'None'
    if request.method == 'POST':
        form = SalesmanRegistrationForm(request.POST)
        form.fields['market'].choices = [(market.id, market.name) for market in markets]
        if form.is_valid():
            user = form.save()
            market = Market.objects.get(id=form.data['market'])
            salesman = Salesman(
                user=user,
                market=market,
            )
            salesman.save()
            return redirect('/login-sale')
        err = 'Invalid input'
    return render(request, 'register_salesman.html', {'form': form, 'error': err})


def register_deliveryman(request):
    form = DeliverymanRegistrationForm()
    err = 'None'
    if request.method == 'POST':
        form = DeliverymanRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            deliveryman = Deliveryman(
                user=user,
            )
            deliveryman.save()
            return redirect('/login-del')
        err = 'Invalid input'
    return render(request, 'register_deliveryman.html', {'form': form, 'error': err})
