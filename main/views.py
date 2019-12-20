from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Phone, Cart
from django.http import JsonResponse


# Create your views here.

def item_list(request):
    if not request.session.session_key:
        request.session.save()
    data = Phone.objects.all()
    item = {}
    try:
        cart = Cart.objects.get(
            user=request.user.username if request.user.is_authenticated else request.session.session_key)
        item = cart.items
    except Cart.DoesNotExist:
        pass
    finally:
        return render(request, 'main_page.html', {'data': data, 'cart': item})


def product(request, id):
    phone = Phone.objects.get(id=id)
    return render(request, 'product.html', {'phone': phone})


@csrf_exempt
def cart_create(request):
    item = request.POST.get('name')
    quantity = request.POST.get('quantity')
    obj = cart_check(request.user.username) if request.user.is_authenticated else cart_check(
        request.session.session_key)
    obj.items[item] = 1
    if not request.user.is_authenticated:
        request.session['cart_id'] = obj.id
        print(request.session['cart_id'])
    for i, j in obj.items.items():
        phone = Phone.objects.get(name=i)
    cost = cart_cost(obj.items)
    obj.cost = cost
    obj.save()
    return JsonResponse({'success': 1})


def view_cart(request):
    try:
        phones = Cart.objects.get(user=request.user.username) if request.user.is_authenticated else Cart.objects.get(
            user=request.session.session_key)
        items = phones.items

    except Cart.DoesNotExist:
        phones = False
    finally:
        return render(request, 'cart.html', {'рhones': phones})


@csrf_exempt
def cart_change(request):
    if request.is_ajax():
        phones = Cart.objects.get(user=request.user.username) if request.user.is_authenticated else Cart.objects.get(
            user=request.session.session_key)
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        phones.items[name] = quantity
        cost = cart_cost(phones.items)
        phones.cost = cost
        phones.save()
        return JsonResponse({'cost': cost})


@csrf_exempt
def cart_delete(request):
    if request.is_ajax():
        phones = Cart.objects.get(user=request.user.username) if request.user.is_authenticated else Cart.objects.get(
            user=request.session.session_key)
        name = request.POST.get('name')
        del phones.items[name]
        cost = cart_cost(phones.items)
        phones.cost = cost
        phones.save()
        return JsonResponse({'cost': cost})


@login_required
def logout(request):
    print(request.user.username)
    logout(request)
    return render(request, 'main_page.html')


# Not views
def cart_cost(cart_item):
    cost = 0
    for i, j in cart_item.items():
        obj = Phone.objects.get(name=i)
        cost += obj.price * int(j)
    return cost


def cart_check(username):
    try:
        cart_obj = Cart.objects.get(user=username)
        return cart_obj
    except Cart.DoesNotExist:
        cart_obj = Cart.objects.create(user=username, items={}, cost=0)
        return cart_obj
