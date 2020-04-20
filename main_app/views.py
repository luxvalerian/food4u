from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.views.generic import CreateView
from .scraper import produce_dict, logo_img, logo_svg, walmart_fruit
from . forms import CustomerSignUpForm, VolunteerSignUpForm
from .models import Item, Cart, Timeslot, Customer, Volunteer
from .decorators import allowed_users


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            group = Group.objects.get(name='customer')

            user = form.save()
            customer_profile = Customer(user=user)
            cart = Cart(user=user)
            cart.save()
            customer_profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.groups.add(group)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = CustomerSignUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def volunteer_signup(request):
    error_message = ''
    if request.method == 'POST':
        form = VolunteerSignUpForm(request.POST)
        if form.is_valid():
            group = Group.objects.get(name='volunteer')
            # print(group)
            user = form.save()
            volunteer_profile = Volunteer(user=user)
            volunteer_profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.groups.add(group)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = VolunteerSignUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup_volunteer.html', context)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
@allowed_users(allowed_roles=['customer'])
def stores(request):
    items = Item.objects.all()
    context = {'product': produce_dict, 'logo': logo_img, 'logo_svg': logo_svg, 'items': items, 'walmart': walmart_fruit}
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


def remove_vol(request):
    return redirect('customer/index.html')


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
    customer = Customer.objects.filter(user=request.user)
    # timeslot = Timeslot.objects.filter(customer=customer)
    # timeslot_count = timeslot.count()
    cart = Cart.objects.filter(user=request.user).all()
    # items_not_in_cart = Item.objects.exclude(id__in = cart.items.all().values_list('id'))
    print(cart.all())
    user_group = str(request.user.groups.all()[0])

    context = {'user_group' : user_group, 'customer': customer, 'cart': cart}
    return render(request, 'cart/cart.html', context)
