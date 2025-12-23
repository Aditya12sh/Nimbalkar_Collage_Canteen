from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # AUTH
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),

    # MAIN
    path('menu/', views.menu, name='menu'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),

    # CHECKOUT FLOW
    path('place-order/', views.place_order, name='place_order'),
    path('payment/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),

    # ORDERS
    path('my-orders/', views.my_orders, name='my_orders'),

    # STATIC
    path('about/', views.about, name='about'),
    path('contact/', views.contactus, name='contactus'),
]
