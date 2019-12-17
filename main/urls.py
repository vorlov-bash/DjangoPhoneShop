from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.item_list, name='main'),
    path('product/<int:id>', views.product, name='product')
]
