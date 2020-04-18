from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.views.generic import CreateView
from .scraper import produce_dict, logo_img, logo_svg

from .models import Item, Cart, Timeslot
from .decorators import allowed_users


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            group = Group.objects.get(name='customer')
            # print(group)
            user = form.save()
            username = form.cleaned_data.get('username')
            user.groups.add(group)

            login(request, user)
            return redirect('stores')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def volunteer_signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            group = Group.objects.get(name='volunteer')
            # print(group)
            user = form.save()
            username = form.cleaned_data.get('username')
            user.groups.add(group)

            login(request, user)
            return redirect('stores')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup_volunteer.html', context)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
@allowed_users(allowed_roles=['customer'])
def stores(request):
    context = {'product': produce_dict, 'logo': logo_img, 'logo_svg': logo_svg}
    return render(request, 'stores/index.html', context)


@login_required
def stores_index(request):
    return render(request, 'stores/index.html')


@login_required
def stores_detail(request):
    return render(request, 'stores/detail.html')


def logout(request):
    return render(request, 'stores/detail.html')


@login_required
@allowed_users(allowed_roles=['admin'])
def remove_vol(request):
    return redirect('customer/index.html')


def remove_vol(request, volunteer_id, cart_id, customer_id, timeslot_id):
    Timeslot.objects.get(id=timeslot_id).volunteers.remove(volunteer_id)
    return redirect('customer/index.html', total_volunteers, total_checkouts)


@login_required
@allowed_users(allowed_roles=['customer'])
def checkout(request): 
    return render(request, 'checkout.html')


def customer_index(request, customer_id):
    customer_id = request.user.id
    context = {'customer_id': customer_id}
    return render(request, 'customer/index.html', context)

@login_required
def cart(request, profile_id):
    timeslot = Timeslot.objects.filter(user=request.user)
    # timeslot = Timeslot.objects.all()
    user_group = str(request.user.groups.all()[0])

    context = {'user_group' : user_group, 'timeslot': timeslot}
    return render(request, 'cart/cart.html', context)
