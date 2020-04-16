from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('stores/', views.stores, name='stores'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('checkout/<int:volunteer_id>/<int:cart_id>/<int:customer_id>/<int:timeslot_id>', views.checkout, name='checkout'),
    path('customer/<int:customer_id>/', views.customer_index, name='customer'),
    path('remove/', views.remove_vol, name='remove'),
    path('accounts/signup/', views.signup, name='signup'),
    path('cart/', views.cart, name='cart'),
]
