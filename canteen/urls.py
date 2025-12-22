from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contactus, name='contactus'),
    path('order/', views.order_page, name='order'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'),

    # Combined login/signup page
    path('login_signup/', views.login_signup, name='login_signup'),
]
