from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.item_list, name='main'),
    path('<int:id>', views.product, name='product'),
    path('cart_create', views.cart_create, name='create'),
    path('logout', views.logout, name='logout'),
    path('cart', views.view_cart, name='cart'),
    path('cart_upd', views.cart_change, name='cart_upd'),
    path('cart_del', views.cart_delete, name='cart_del')

]
