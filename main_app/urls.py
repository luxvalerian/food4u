from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('stores/', views.stores, name='stores'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    # path('login/volunteer/',
    #      views.volunteer_login, name='volunteer_login'),
    path('checkout/', views.checkout, name='checkout'),
    path('customer/<int:customer_id>/', views.customer_index, name='customer'),
    path('remove/', views.remove_vol, name='remove'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signup/volunteer',
         views.volunteer_signup, name='volunteer_signup'),
    path('cart/<int:profile_id>', views.cart, name='cart'),
]
