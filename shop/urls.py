from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart, name='cart'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    path('remove-from-cart/<int:id>/<str:color>/', views.remove_from_cart),
        
    path('checkout/', views.checkout, name='checkout'),

    path('success/', views.success, name='success'),

    path('register/', views.register),

    path('login/', views.user_login),
    
    path('logout/', views.user_logout),
]