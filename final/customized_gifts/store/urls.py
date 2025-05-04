from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('signup/', views.signup, name='signup'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),  
    path('remove-from-cart/<int:index>/', views.remove_from_cart, name='remove_from_cart'),
]
