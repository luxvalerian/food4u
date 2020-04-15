from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('stores/', views.stores, name='stores'),
<<<<<<< HEAD
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('checkout/<int:total_volunteers>/<int:total_checkouts>/', views.checkout, name='checkout'),
    path('remove/', views.remove_vol, name='remove'),
    path('accounts/signup/', views.signup, name='signup'),

=======
    path('accounts/signup/', views.signup, name='signup'),
    path('checkout/<int:total_volunteers>/<int:total_checkouts>/',
         views.checkout, name='checkout'),
    path('remove/', views.remove_vol, name='remove'),
>>>>>>> ee92a683d91b0e2e2f19172ca20c665c127e59e5
]
