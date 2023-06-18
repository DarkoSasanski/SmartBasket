from django.contrib import admin
from SmartBasket.models import *


# Register your models here.

class CategoryAdmin(admin.StackedInline):
    model = Category
    extra = 0


class MarketAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone_number", "email",)
    inlines = [CategoryAdmin, ]

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and Salesman.objects.filter(user=request.user, market=obj).exists():
            return True
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if Salesman.objects.filter(user=request.user).exists():
            salesmen = Salesman.objects.get(user=request.user)
            return qs.filter(id=salesmen.market.id)
        return qs


admin.site.register(Market, MarketAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "phone_number",)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.user == request.user:
            return True
        return False


admin.site.register(Customer, CustomerAdmin)


class SalesmanAdmin(admin.ModelAdmin):
    list_display = ("user", "market",)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.user == request.user:
            return True
        return False


admin.site.register(Salesman, SalesmanAdmin)


class DeliverymanAdmin(admin.ModelAdmin):
    list_display = ("user",)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.user == request.user:
            return True
        return False


admin.site.register(Deliveryman, DeliverymanAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity",)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and Salesman.objects.filter(user=request.user, market=obj.category.market).exists():
            return True
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            # Filter the queryset for the foreign key field
            if Salesman.objects.filter(user=request.user).exists():
                salesmen = Salesman.objects.get(user=request.user)
                kwargs['queryset'] = Category.objects.filter(market=salesmen.market)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Product, ProductAdmin)


class ShoppingCartItemAdmin(admin.StackedInline):
    model = ShoppingCartItem
    extra = 0


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("customer", "market", )
    readonly_fields = ("customer", )
    inlines = [ShoppingCartItemAdmin, ]

    def has_add_permission(self, request):
        if Customer.objects.filter(user=request.user).exists():
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.customer.user == request.user:
            return True
        return False

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.customer = Customer.objects.get(user=request.user)
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if Salesman.objects.filter(user=request.user).exists():
            salesmen = Salesman.objects.get(user=request.user)
            return qs.filter(market=salesmen.market)
        return qs.filter(customer__user=request.user)


admin.site.register(ShoppingCart, ShoppingCartAdmin)


class PickUpOrderItemAdmin(admin.StackedInline):
    model = PickUpOrderItem
    extra = 0


class PickUpOrderAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_pickup", "phone_number", "market", )
    inlines = [PickUpOrderItemAdmin, ]

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and Salesman.objects.filter(user=request.user).exists():
            salesmen = Salesman.objects.get(user=request.user)
            return obj.market == salesmen.market
        return False


admin.site.register(PickUpOrder, PickUpOrderAdmin)


class DeliveryOrderItemAdmin(admin.StackedInline):
    model = DeliveryOrderItem
    extra = 0


class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "address", "phone_number", "market", "payment_option", "deliveryman", )
    inlines = [DeliveryOrderItemAdmin, ]

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and Salesman.objects.filter(user=request.user).exists():
            salesmen = Salesman.objects.get(user=request.user)
            return obj.market == salesmen.market
        if obj and obj.deliveryman.user == request.user:
            return True
        return False


admin.site.register(DeliveryOrder, DeliveryOrderAdmin)