from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import *
from .models import *
import random


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
        err = 'Невалидно корисничко име или лозинка'
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
                    return redirect('/sale-products')
        err = 'Невалидно корисничко име или лозинка'
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
                    return redirect('/deliveryman-orders')
        err = 'Невалидно корисничко име или лозинка'
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
        err = 'Невалиден влез'
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
        err = 'Невалиден влез'
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
        err = 'Невалиден влез'
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
                              {'product': product, 'error': 'Веќе имате креирано кошничка во друга продавница'})
            cart_item = ShoppingCartItem.objects.filter(shopping_cart=cart, product=product).first()
            if int(request.POST.get('quantity')) > product.quantity:
                return render(request, 'product_details.html', {'product': product, 'error': 'Недоволно достапни продукти'})
            if cart_item is None:
                cart_item = ShoppingCartItem(shopping_cart=cart, product=product,
                                             quantity=int(request.POST.get('quantity')))
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
                return render(request, 'list_shopping_cart.html', {'cart': cart, 'error': 'Вашата кошница е празна'})
            cart_items = ShoppingCartItem.objects.filter(shopping_cart=cart).all()
            total = 0
            for cart_item in cart_items:
                total += cart_item.product.price * cart_item.quantity
            return render(request, 'list_shopping_cart.html', {'cart': cart, 'cart_items': cart_items, 'error': 'None',
                                                               'total': total})
    return redirect('/login-cust')


def delete_cart(request):
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user).exists():
            customer = Customer.objects.get(user=request.user)
            cart = ShoppingCart.objects.filter(customer=customer).first()
            if cart is None:
                return redirect('/markets')
            cart_items = ShoppingCartItem.objects.filter(shopping_cart=cart).all()
            for cart_item in cart_items:
                product = cart_item.product
                product.quantity += cart_item.quantity
                product.save()
            cart.delete()
    return redirect('/markets')


def delete_cart_item(request, cart_item_id):
    cart_item = ShoppingCartItem.objects.get(id=cart_item_id)
    product = cart_item.product
    product.quantity += cart_item.quantity
    product.save()
    cart_item.delete()
    return redirect('/shopping-cart')


def create_pickup_order(request):
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user).exists():
            customer = Customer.objects.get(user=request.user)
            cart = ShoppingCart.objects.filter(customer=customer).first()
            if cart is None:
                return redirect('/markets')
            cart_items = ShoppingCartItem.objects.filter(shopping_cart=cart).all()
            total = 0
            for cart_item in cart_items:
                total += cart_item.product.price * cart_item.quantity
            form = PickUpOrderForm()
            form.initial['first_name'] = customer.user.first_name
            form.initial['last_name'] = customer.user.last_name
            form.initial['phone_number'] = customer.phone_number
            if request.method == 'POST':
                f = PickUpOrderForm(request.POST)
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
                    return render(request, "success_order.html")
            return render(request, 'create_pickup_order.html', {'cart': cart, 'cart_items': cart_items,
                                                                'total': total, 'form': form})
    return redirect('/login-cust')


def create_delivery_order(request):
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user).exists():
            customer = Customer.objects.get(user=request.user)
            cart = ShoppingCart.objects.filter(customer=customer).first()
            if cart is None:
                return redirect('/markets')
            cart_items = ShoppingCartItem.objects.filter(shopping_cart=cart).all()
            total = 0
            for cart_item in cart_items:
                total += cart_item.product.price * cart_item.quantity
            form = DeliveryOrderForm()
            form.initial['first_name'] = customer.user.first_name
            form.initial['last_name'] = customer.user.last_name
            form.initial['phone_number'] = customer.phone_number
            form.initial['address'] = customer.address
            if request.method == 'POST':
                f = DeliveryOrderForm(request.POST)
                if f.is_valid():
                    order = DeliveryOrder(
                        first_name=f.cleaned_data['first_name'],
                        last_name=f.cleaned_data['last_name'],
                        phone_number=f.cleaned_data['phone_number'],
                        address=f.cleaned_data['address'],
                        payment_option=f.cleaned_data['payment_option'],
                        market=cart.market,
                        delivered=False
                    )
                    order.save()
                    for cart_item in cart_items:
                        order_item = DeliveryOrderItem(
                            order=order,
                            product=cart_item.product,
                            quantity=cart_item.quantity,
                        )
                        order_item.save()
                    cart.delete()
                    if order.payment_option == 'online':
                        return redirect('/payment')
                    return render(request, "success_order.html")
            return render(request, 'create_delivery_order.html', {'cart': cart, 'cart_items': cart_items,
                                                                  'total': total, 'form': form})
    return redirect('/login-cust')


def payment(request):
    form = PaymentForm()
    if request.method == 'POST':
        f = PaymentForm(request.POST)
        if f.is_valid():
            return render(request, 'success_order.html')
    return render(request, 'payment.html', {'form': form})


def list_products_for_salesman(request):
    if request.user.is_authenticated:
        if Salesman.objects.filter(user=request.user).exists():
            salesman = Salesman.objects.get(user=request.user)
            search = request.GET.get('search')
            if search is None or search == '':
                products = Product.objects.filter(category__market=salesman.market).all()
            else:
                products = Product.objects.filter(category__market=salesman.market, name__icontains=search).all()
            return render(request, 'list_products_for_salesman.html', {'products': products, 'search': search, 'market' : salesman.market})
    return redirect('/login-sale')


def sale_product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'sale_product_details.html', {'product': product, 'error': 'None'})


def update_quantity(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        new_quantity = request.POST.get('quantity')
        product.quantity = new_quantity
        product.save()
    return redirect('/sale-product-details/' + str(product_id))


def add_new_product(request):
    if request.user.is_authenticated:
        if Salesman.objects.filter(user=request.user).exists():
            salesman = Salesman.objects.get(user=request.user)
            form = AddProductForm()
            categories = Category.objects.filter(market=salesman.market).all()
            form.fields['category'].choices = [(category.id, category.name) for category in categories]
            if request.method == 'POST':
                f = AddProductForm(request.POST, request.FILES)
                form.fields['category'].choices = [(category.id, category.name) for category in categories]
                if f.is_valid():
                    product = f.save(commit=False)
                    product.image = f.cleaned_data['image']
                    product.save()
                    return render(request, 'success_product.html')
            return render(request, 'add_new_product.html', {'form': form})
    return redirect('/login-sale')


def list_orders(request):
    if request.user.is_authenticated:
        if Salesman.objects.filter(user=request.user).exists():
            salesman = Salesman.objects.get(user=request.user)
            pickup_orders = PickUpOrder.objects.filter(market=salesman.market).all()
            delivery_orders = DeliveryOrder.objects.filter(market=salesman.market).all()
            return render(request, 'list_orders.html',
                          {'pickup_orders': pickup_orders, 'delivery_orders': delivery_orders})
    return redirect('/login-sale')


def pickup_order_details(request, order_id):
    order = PickUpOrder.objects.get(id=order_id)
    order_items = PickUpOrderItem.objects.filter(order=order).all()
    total = 0
    for order_item in order_items:
        total += order_item.product.price * order_item.quantity
    return render(request, 'pickup_order_details.html', {'order': order, 'order_items': order_items, 'total': total})


def delivery_order_details(request, order_id):
    order = DeliveryOrder.objects.get(id=order_id)
    order_items = DeliveryOrderItem.objects.filter(order=order).all()
    total = 0
    for order_item in order_items:
        total += order_item.product.price * order_item.quantity
    return render(request, 'delivery_order_details.html', {'order': order, 'order_items': order_items, 'total': total})


def assign_order(request, order_id):
    delivery_men = Deliveryman.objects.all()
    order = DeliveryOrder.objects.get(id=order_id)
    if request.method == 'POST':
        deliveryman_id = request.POST.get('deliveryman')
        deliveryman = Deliveryman.objects.get(id=deliveryman_id)
        order = DeliveryOrder.objects.get(id=order_id)
        order.deliveryman = deliveryman
        order.save()
        return redirect('/delivery-order-details/' + str(order_id))
    return render(request, 'assign_order.html', {'delivery_men': delivery_men, "order": order})


def mark_as_picked_up(request, order_id):
    order = PickUpOrder.objects.get(id=order_id)
    order.picked_up = True
    order.save()
    return redirect('/pickup-order-details/' + str(order_id))


def delivery_man_orders(request):
    if request.user.is_authenticated:
        if Deliveryman.objects.filter(user=request.user).exists():
            deliveryman = Deliveryman.objects.get(user=request.user)
            orders = DeliveryOrder.objects.filter(deliveryman=deliveryman).all()
            return render(request, 'deliveryman_orders.html', {'orders': orders})


def deliveryman_order_details(request, order_id):
    order = DeliveryOrder.objects.get(id=order_id)
    order_items = DeliveryOrderItem.objects.filter(order=order).all()
    total = 0
    for order_item in order_items:
        total += order_item.product.price * order_item.quantity
    return render(request, 'deliveryman_order_details.html',
                  {'order': order, 'order_items': order_items, 'total': total})


def mark_as_delivered(request, order_id):
    order = DeliveryOrder.objects.get(id=order_id)
    order.delivered = True
    order.save()
    return redirect('/deliveryman-order-details/' + str(order_id))


def logout(request):
    auth.logout(request)
    return redirect('/')
