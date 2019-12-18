from django.contrib import admin
from .models import Phone, Cart


# Register your models here.


class PhoneAdmin(admin.ModelAdmin):
    readonly_fields = ['image_tag']
    list_display = ('name', 'quantity', 'price')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'item_items', 'item_cost')


admin.site.register(Phone, PhoneAdmin)
admin.site.register(Cart, CartAdmin)
