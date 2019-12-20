from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.item_list, name='main'),
    path('<int:id>', views.product, name='product'),
    path('cart_create', views.cart_create, name='create'),
    path('cart', views.view_cart, name='cart'),
    path('cart_upd', views.cart_change, name='cart_upd'),
    path('cart_del', views.cart_delete, name='cart_del'),
    path('auth', views.is_auth, name='auth'),
    path('favo', views.favo_load, name='favo_load'),
    path('favo_upd', views.favo, name='favo_upd')

]
