from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.item_list, name='main'),
    path('<int:id>', views.product, name='product'),
    path('cart_add', views.cart_add, name='add'),
    path('logout', views.logout, name='logout')

]
