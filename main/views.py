from django.shortcuts import render
from .models import Phone


# Create your views here.

def item_list(request):
    data = Phone.objects.all()
    print(data)
    return render(request, 'main_page.html', {'data': data})


def test(request):
    return render(request, 'test.html')


def product(request, id):
    phone = Phone.objects.get(id=id)
    return render(request, 'product.html', {'phone': phone})
