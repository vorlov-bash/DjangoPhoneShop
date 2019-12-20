from django import template
from ..models import Cart, Phone

register = template.Library()


@register.filter
def range_array(int_var):
    arr = [str(i) for i in range(1, int(int_var) + 1)]
    print(arr)
    return arr


@register.filter
def id(name):
    return Phone.objects.get(name=name).id


@register.filter
def about(name):
    return Phone.objects.get(name=name).about


@register.filter
def quantity(name):
    return Phone.objects.get(name=name).quantity


@register.filter
def price(name):
    return Phone.objects.get(name=name).price


@register.filter
def image(name):
    return Phone.objects.get(name=name).image


@register.filter
def cost_count(name, quantity):
    price = Phone.objects.get(name=name).price
    return int(quantity) * int(price)


@register.filter
def total(name):
    return int(name) + 40


@register.filter
def instock(name):
    stock = bool(Phone.objects.get(name=name).quantity)
    return stock



