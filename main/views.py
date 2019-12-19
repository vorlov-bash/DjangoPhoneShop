from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Phone, Cart
from django.http import JsonResponse


# Create your views here.

def item_list(request):
    data = Phone.objects.all()
    print(data)
    if not request.session.session_key:
        request.session.save()
    return render(request, 'main_page.html', {'data': data})


def product(request, id):
    phone = Phone.objects.get(id=id)
    return render(request, 'product.html', {'phone': phone})


@csrf_exempt
def cart_add(request):
    item = request.POST.get('name')
    obj = cart_check(request.user.username) if request.user.is_authenticated else request.session.session_key
    if item in obj.items:
        obj.items[item] += 1
    else:
        obj.items[item] = 1
    if request.user.is_authenticated:
        request.session['cart_id'] = obj.id
    obj.save()
    return JsonResponse({'success': 1})


@login_required
def logout(request):
    print(request.user.username)
    logout(request)
    return render(request, 'main_page.html')


# Not views
def cart_check(username):
    try:
        cart_obj = Cart.objects.get(user=username)
        return cart_obj
    except Cart.DoesNotExist:
        cart_obj = Cart.objects.create(user=username, items={}, cost=0)
        return cart_obj
