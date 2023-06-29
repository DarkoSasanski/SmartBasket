"""Domasna5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Domasna5 import settings
from SmartBasket.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path("index", index, name="index"),
    path("login-cust", login_customer, name="login-cust"),
    path("login-sale", login_salesman, name="login-sale"),
    path("login-del", login_deliveryman, name="login-del"),
    path("register-cust", register_customer, name="register-cust"),
    path("register-sale", register_salesman, name="register-sale"),
    path("register-del", register_deliveryman, name="register-del"),
    path('markets', list_markets, name='markets'),
    path('categories/<str:market_id>', list_categories_for_market, name='categories'),
    path('products/<str:category_id>', list_products_for_category, name='products'),
    path('product-detail/<str:product_id>', product_details, name='product'),
    path('add-to-cart/<str:product_id>', add_to_cart, name='add-to-cart'),
    path('shopping-cart', list_shopping_cart, name='shopping-cart'),
    path('empty-cart', delete_cart, name='empty-cart'),
    path('delete-cart-item/<str:cart_item_id>', delete_cart_item, name='delete-cart-item'),
    path('create-pickup-order', create_pickup_order, name='create-pickup-order'),
    path('create-delivery-order', create_delivery_order, name='create-delivery-order'),
    path('payment', payment, name='payment'),
    path('sale-products', list_products_for_salesman, name='sale-products'),
    path('sale-product-details/<str:product_id>', sale_product_details, name='sale-product'),
    path('update-quantity/<str:product_id>', update_quantity, name='update-quantity'),
    path('add-product', add_new_product, name='add-product'),
    path('orders', list_orders, name='orders'),
    path('pickup-order-details/<str:order_id>', pickup_order_details, name='pickup-order-details'),
    path('delivery-order-details/<str:order_id>', delivery_order_details, name='delivery-order-details'),
    path('assign-order/<str:order_id>', assign_order, name='assign-order'),
    path('mark-as-picked-up/<str:order_id>', mark_as_picked_up, name='mark-as-picked-up'),
    path('deliveryman-orders', delivery_man_orders, name='deliveryman-orders'),
    path('mark-as-delivered/<str:order_id>', mark_as_delivered, name='mark-as-delivered'),
    path('deliveryman-order-details/<str:order_id>', deliveryman_order_details, name='deliveryman-order-details'),
    path('logout', logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
