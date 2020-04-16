from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .scraper import produce_dict, logo_img, logo_svg
from .models import Item, Cart, Volunteer, Customer, User, Timeslot


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def stores(request):
    context = {'product': produce_dict, 'logo': logo_img, 'logo_svg': logo_svg}
    return render(request, 'stores/index.html', context)


def stores_index(request):
    return render(request, 'stores/index.html')


def stores_detail(request):
    return render(request, 'stores/detail.html')

def logout(request):
    return render(request, 'stores/detail.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('stores')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def remove_vol(request, volunteer_id, cart_id, customer_id, timeslot_id):
    Timeslot.objects.get(id=timeslot_id).volunteers.remove(volunteer_id)
    
    return redirect('customer/index.html', total_volunteers, total_checkouts)

def checkout(request, volunteer_id, cart_id, customer_id, timeslot_id):
    volunteer = Volunteer.objects.get(id=volunteer_id)
    customer = Customer.objects.get(id=customer_id)
    timeslot = Customer.objects.get(id=timeslot_id)
    cart = Cart.objects.get(id=cart_id)
    
    context = {"volunteer": volunteer, "customer": customer, "timeslot": timeslot, "cart": cart}
    return render(request, 'checkout.html', customer_id=customer_id)

def customer_index(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    context = {'customer': customer}
    return render(request, 'customer/index.html', context)