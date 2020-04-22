from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import Group

from datetime import date
from .scraper import produce_dict, logo_img, walmart_fruit
from . forms import CustomerSignUpForm, VolunteerSignUpForm
from .models import Item, Cart, Timeslot, Customer, Volunteer
from .decorators import allowed_users


# def login(request):
#     volunteer = Volunteer.objects.all()
#     context = {'volunteer': volunteer}
#     if volunteer.filter(id=request.user.id):
#         return render(request, 'profile.html', context)
#     else:
#         return render(request, 'stores', context)


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
            return redirect('profile')
        else:
            error_message = 'Invalid sign up - try again'
    form = CustomerSignUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def volunteer_signup(request):
    error_message = ''
    if request.method == 'POST':
        form = VolunteerSignUpForm(request.POST)
        for time in form:
            print(time)
        if form.is_valid():
            group = Group.objects.get(name='volunteer')
            # print(group)
            user = form.save()
            volunteer_profile = Volunteer(user=user)
            print(volunteer_profile)
            volunteer_profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.groups.add(group)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid sign up - try again'
    form = VolunteerSignUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup_volunteer.html', context)


# def volunteer_login(request):
#     error_message = ''
#     if request.method == 'GET':
#         form = VolunteerLogInForm(request.GET)
#         # if form.is_valid():
#         #     group = Group.objects.get(name='volunteer')
#         #     # user = form.save()
#         #     volunteer_profile = Volunteer(user=user)
#         #     # volunteer_profile.save()
#         #     username = form.cleaned_data.get('username')
#         #     raw_password = form.cleaned_data.get('password1')
#         #     # user.groups.add(group)
#         user = authenticate(username=username, password=raw_password)
#         login(request, user)
#         return redirect('profile')
#     else:
#         error_message = 'Invalid sign up - try again'
#     form = VolunteerLogInForm()
#     context = {'form': form, 'error_message': error_message}
#     return render(request, 'registration/login_volunteer.html', context)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def profile(request):
    return render(request, 'account/profile.html')


@login_required
@allowed_users(allowed_roles=['customer'])
def stores(request):
    items = Item.objects.all()
    context = {'product': produce_dict, 'logo': logo_img,
               'items': items, 'walmart': walmart_fruit}
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


@login_required
@allowed_users(allowed_roles=['customer'])
def checkout(request):

    customer = Customer.objects.filter(user=request.user)
    active_customer = customer.first()
    customer_delivery_time = active_customer.delivery_time
    customer_delivery_date = date.today()
    timeslot = None
    customer_time = None
    customer_date = None
    if Timeslot.objects.all():
        timeslot = Timeslot.objects.filter(customer__in=customer)
        for time in timeslot:
            customer_time = time.timeslot
            customer_date = time.date
    available = None
    available_date = None
    helpers = None
    volunteer = Volunteer.objects.all()
    for helper in volunteer:
        for help_time in helper.availability:
            for time in customer_delivery_time:
                if time == help_time and customer_delivery_date == helper.availability_date:
                    available = time
                    helpers = helper
                    available_date = helper.availability_date
    error_message = ''

    if available in customer_delivery_time and customer_delivery_date == available_date:
        new_timeslot = Timeslot(date=customer_delivery_date,
                                timeslot=available, customer=active_customer, volunteer=helpers)
        check_timeslots = Timeslot.objects.filter(
            date=customer_delivery_date, timeslot=available, customer=active_customer, volunteer=helpers)
        if check_timeslots.exists():
            dupe_timeslot = check_timeslots.first()
            if new_timeslot.timeslot == dupe_timeslot.timeslot and new_timeslot.volunteer == dupe_timeslot.volunteer and new_timeslot.customer == dupe_timeslot.customer and new_timeslot.date == dupe_timeslot.date:
                error_message = 'Sorry No Volunteers Are Available To Deliver At This Time'
            else:
                new_timeslot.save()
        else:
            new_timeslot.save()
            # error_message = 'Return an Else'
    else:
        error_message = 'Sorry No Volunteers Are Available To Deliver At This Time'
        print(error_message)
    context = {'customer': customer, 'timeslot': timeslot,
               'error': error_message, 'vol_time': volunteer}
    return render(request, 'checkout.html', context)


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

    context = {'user_group': user_group, 'customer': customer, 'cart': cart}
    return render(request, 'account/cart.html', context)


class CustomerDeliveryTimeUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['delivery_time']
