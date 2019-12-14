from django.shortcuts import render
from .models import Phone


# Create your views here.

def item_list(request):
    data = Phone.objects.all()
    return render(request, 'main_page.html', {'data': data})


def test(request):
    return render(request, 'test.html')
