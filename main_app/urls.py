from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('stores/', views.stores_index, name='index'),
    path('stores/detail/', views.stores_detail, name='detail'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    # path('login/volunteer/',
    #      views.volunteer_login, name='volunteer_login'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove/', views.remove_vol, name='remove'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signup/volunteer', views.volunteer_signup, name='volunteer_signup'),
    path('cart/<int:user_id>', views.cart, name='cart'),
    path('customer/<int:pk>/update/', views.CustomerUpdate.as_view(), name="customer_update"),
    path('volunteer/<int:pk>/update/', views.VolunteerUpdate.as_view(), name="volunteer_update"),
    # path('checkout/<int:profile_id>', views.cart, name='add_timeslot')
]
