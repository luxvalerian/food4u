from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('stores/', views.stores, name='stores'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('checkout/', views.checkout, name='checkout'),
    path('customer/', views.customer_index, name='customer'),
    path('remove/', views.remove_vol, name='remove'),
    path('accounts/signup/', views.signup, name='signup'),
    path('cart/', views.cart, name='cart'),
    path('accounts/signup/volunteer/', views.VolunteerSignUpView.as_view(), name='volunteer_signup'),
    path('accounts/signup/customer/', views.customer_signup, name='customer_signup')
    # path('accounts/signup/customer/', views.CustomerSignUpView.as_view(), name='customer_signup')
]
