from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Phone, Cart, Favorites
from django.http import JsonResponse
import smtplib
import requests
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Create your views here.

def item_list(request):
    if not request.session.session_key:
        request.session.save()
    data = Phone.objects.all()
    cart = {}
    item = {}
    favo = {}
    try:
        cart = Cart.objects.get(
            user=request.user.username if request.user.is_authenticated else request.session.session_key)
        favo = Favorites.objects.get(
            user=request.user.username if request.user.is_authenticated else request.session.session_key)
        item = cart.items
    except Cart.DoesNotExist or Favorites.DoesNotExist:
        pass
    finally:
        return render(request, 'main_page.html', {'data': data, 'cart': item, 'favo': favo.items})


def product(request, id):
    cart = {}
    phone = {}
    try:
        phone = Phone.objects.get(id=id)
        cart = Cart.objects.get(
            user=request.user.username if request.user.is_authenticated else request.session.session_key)
    except Cart.DoesNotExist:
        pass
    finally:
        return render(request, 'product.html', {'phone': phone, 'cart': cart.items})


def favo_load(request):
    obj = favo_check(request.user.username) if request.user.is_authenticated else favo_check(
        request.session.session_key)
    print(obj.items)
    return render(request, 'favo.html', {'data': obj.items})


@csrf_exempt
def favo(request):
    item = request.POST.get('name')
    obj = favo_check(request.user.username) if request.user.is_authenticated else favo_check(
        request.session.session_key)
    if int(request.POST.get('add')):
        obj.items.append(item)
        if not request.user.is_authenticated:
            request.session['array_id'] = obj.id
    elif not int(request.POST.get('add')):
        print(obj.items)
        obj.items.remove(item)
        print(obj.items)
        obj.save()
        if not request.user.is_authenticated:
            request.session['array_id'] = obj.id
    obj.save()
    return JsonResponse({})


@csrf_exempt
def is_auth(request):
    if request.user.is_authenticated:
        return JsonResponse({'auth': 1})
    else:
        return JsonResponse({'auth': 0})


@csrf_exempt
def cart_create(request):
    item = request.POST.get('name')
    obj = cart_check(request.user.username) if request.user.is_authenticated else cart_check(
        request.session.session_key)
    obj.items[item] = 1
    if not request.user.is_authenticated:
        request.session['cart_id'] = obj.id
    cost = cart_cost(obj.items)
    obj.cost = cost
    obj.save()
    if request.POST.get('delete'):
        favo = favo_check(request.user.username) if request.user.is_authenticated else favo_check(
            request.session.session_key)
        favo.items.remove(item)
        print(favo.items)
        favo.save()
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
        phone = Phone.objects.get(name=name)
        del phones.items[name]
        print(phones.items)
        cost = cart_cost(phones.items)
        print(cost)
        phones.cost = cost
        phones.save()
        phone.save()
        return JsonResponse({'cost': cost})


def checkout(request):
    phones = Cart.objects.get(user=request.user.username) if request.user.is_authenticated else Cart.objects.get(
        user=request.session.session_key)
    for i, j in phones.items.items():
        phone = Phone.objects.get(name=i)
        phone.quantity -= int(j)
        phone.save()
    return render(request, 'checkout.html')


def checkout_finish(request):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "volodya.webpr@gmail.com"  # Enter your address
    receiver_email = request.POST.get('email')  # Enter receiver address
    password = 'eniOODD2qg'
    html = '<h1>Дякуємо за заказ:<h1><p></p>'
    x = Cart.objects.get(user=request.session.session_key)
    for i, j in x.items.items():
        html += f'<h3><stong>{i}: {j}</stong></h3><p></p>'
    html += f'<h2>Загальна вартість: {x.cost}</h2>'
    x.delete()
    print(html)
    msg = MIMEMultipart('alternative')
    part0 = MIMEText(html, 'html')
    msg.attach(part0)
    msg["From"] = 'ShopCog'
    msg["To"] = request.POST.get('firstName') + ' ' + request.POST.get('lastName')
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    return redirect('/cart')


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


def favo_check(username):
    try:
        favo_obj = Favorites.objects.get(user=username)
        return favo_obj
    except Favorites.DoesNotExist:
        favo_obj = Favorites.objects.create(user=username, items=[])
        return favo_obj
