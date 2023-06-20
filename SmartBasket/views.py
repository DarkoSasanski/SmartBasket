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
                    return redirect('/markets')
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


def list_markets(request):
    search = request.GET.get('search')
    if search is None or search == '':
        markets = Market.objects.all()
    else:
        markets = Market.objects.filter(name__icontains=search).all()
    return render(request, 'list_markets.html', {'markets': markets, 'search': search})


def list_categories_for_market(request, market_id):
    search = request.GET.get('search')
    market = Market.objects.get(id=market_id)
    if search is None or search == '':
        categories = Category.objects.filter(market=market).all()
    else:
        categories = Category.objects.filter(market=market, name__icontains=search).all()
    return render(request, 'list_categories_for_market.html',
                  {'categories': categories, 'market': market, 'search': search})


def list_products_for_category(request, category_id):
    search = request.GET.get('search')
    category = Category.objects.get(id=category_id)
    if search is None or search == '':
        products = Product.objects.filter(category=category).all()
    else:
        products = Product.objects.filter(category=category, name__icontains=search).all()
    return render(request, 'list_products_for_category.html',
                  {'products': products, 'category': category, 'search': search})


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_details.html', {'product': product, 'error': 'None'})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user).exists():
            customer = Customer.objects.get(user=request.user)
            cart = ShoppingCart.objects.filter(customer=customer).first()
            if cart is None:
                cart = ShoppingCart(customer=customer, market=product.category.market)
                cart.save()
            elif cart.market != product.category.market:
                return render(request, 'product_details.html',
                              {'product': product, 'error': 'Already has a shopping cart for a different market'})
            cart_item = ShoppingCartItem.objects.filter(shopping_cart=cart, product=product).first()
            if int(request.POST.get('quantity')) > product.quantity:
                return render(request, 'product_details.html', {'product': product, 'error': 'Not enough quantity'})
            if cart_item is None:
                cart_item = ShoppingCartItem(shopping_cart=cart, product=product, quantity=int(request.POST.get('quantity')))
            else:
                cart_item.quantity += int(request.POST.get('quantity'))
            product.quantity -= int(request.POST.get('quantity'))
            product.save()
            cart_item.save()
            return redirect('/categories/' + str(product.category.market.id))
    return redirect('/login-cust')


def list_shopping_cart(request):
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user).exists():
            customer = Customer.objects.get(user=request.user)
            cart = ShoppingCart.objects.filter(customer=customer).first()
            if cart is None:
                return render(request, 'list_shopping_cart.html', {'cart': cart, 'error': 'No shopping cart'})
            cart_items = ShoppingCartItem.objects.filter(shopping_cart=cart).all()
            total = 0
            for cart_item in cart_items:
                total += cart_item.product.price * cart_item.quantity
            return render(request, 'list_shopping_cart.html', {'cart': cart, 'cart_items': cart_items, 'error': 'None',
                                                               'total': total})
    return redirect('/login-cust')


def delete_cart(request, cart_id):
    cart = ShoppingCart.objects.get(id=cart_id)
    cart.delete()
    return redirect('/markets')


def delete_cart_item(request, cart_item_id):
    cart_item = ShoppingCartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('/shopping-cart')


def create_pickup_order(request):
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user).exists():
            customer = Customer.objects.get(user=request.user)
            cart = ShoppingCart.objects.filter(customer=customer).first()
            if cart is None:
                return redirect('/shopping-cart')
            cart_items = ShoppingCartItem.objects.filter(shopping_cart=cart).all()
            total = 0
            for cart_item in cart_items:
                total += cart_item.product.price * cart_item.quantity
            if request.method == 'POST':
                f=PickUpOrderForm(request.POST)
                if f.is_valid():
                    order = PickUpOrder(
                        first_name=f.cleaned_data['first_name'],
                        last_name=f.cleaned_data['last_name'],
                        phone_number=f.cleaned_data['phone_number'],
                        date_of_pickup=f.cleaned_data['date_of_pickup'],
                        market=cart.market,
                        picked_up=False
                    )
                    order.save()
                    for cart_item in cart_items:
                        order_item = PickUpOrderItem(
                            order=order,
                            product=cart_item.product,
                            quantity=cart_item.quantity,
                        )
                        order_item.save()
                    cart.delete()
                    return redirect('/success_order')
            return render(request, 'create_pickup_order.html', {'cart': cart, 'cart_items': cart_items,
                                                                'total': total, 'form': PickUpOrderForm()})
    return redirect('/login-cust')
