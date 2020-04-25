from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import Group
from django.urls import reverse
from datetime import date

from .scraper import logo_img, walmart_fruit, produce_dict
from . forms import CustomerSignUpForm, VolunteerSignUpForm, UserUpdateForm, EditCustomerForm
from .models import Item, Cart, Timeslot, Customer, Volunteer, User, Store, Photo
from .decorators import allowed_users

import uuid
import boto3


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'foodle'


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
            user_id = user.id
            return redirect('index')
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
            user_id = user.id
            return redirect('profile', user_id=user_id)
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


# @login_required
# def profile(request, user_id, *kwargs):
#     customer = Customer.objects.filter(user=request.user)
#     volunteer = Volunteer.objects.all()
#     photo = Photo.objects.filter(user=request.user)
#     vol = None
#     for person in volunteer:
#         vol = person

#     vol_timeslot = Timeslot.objects.filter(volunteer__in=volunteer)
#     cus_timeslot = Timeslot.objects.filter(customer__in=customer)

#     context = {'user_id': user_id, 'customer': customer, 'volunteer': volunteer,
#                'vol_timeslot': vol_timeslot, 'cus_timeslot': cus_timeslot, 'photo': photo}
#     return render(request, 'account/profile.html', context)


@login_required
def stores_index(request):
    stores = Store.objects.all()

    context = {'stores': stores}
    return render(request, 'stores/index.html', context)


@login_required
def stores_detail(request, store_name):
    customer = Customer.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user).all()
    user_group = str(request.user.groups.all()[0])
    product_total = 0
    for obj in cart:
        for product in obj.items.all():
            item = Item.objects.filter(id=product.id)
            piece = item.first()
            store_item = piece.store.name
            prices = round(piece.unit_price, 2)
            product_total += piece.count_ref * prices

    stores = Store.objects.all()
    store = stores.filter(name=store_name).first()
    items = Item.objects.filter(store=store)
    context = {'product': produce_dict, 'logo': logo_img,
               'items': items, 'store': store, 'user_group': user_group, 'customer': customer,
               'cart': cart, 'product_total': round(product_total, 2), 'store_item': store_item}
    return render(request, 'stores/detail.html', context)


def logout(request):
    return render(request, 'home.html')


@login_required
@allowed_users(allowed_roles=['admin'])
def remove_vol(request):
    return redirect('customer/index.html')


@login_required
@allowed_users(allowed_roles=['customer'])
def checkout(request, user_id):

    customer = Customer.objects.filter(user=request.user)
    active_customer = customer.first()
    customer_delivery_time = active_customer.delivery_time
    customer_delivery_date = date(2020, 4, 29)  # date.today()
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


@login_required
def cart(request, user_id):
    customer = Customer.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user).all()
    user_group = str(request.user.groups.all()[0])
    product_total = 0
    store_item = None
    for obj in cart:
        for product in obj.items.all():
            item = Item.objects.filter(id=product.id)
            piece = item.first()
            store_item = piece.store.name
            prices = round(piece.unit_price, 2)
            product_total += piece.count_ref * prices
    context = {'user_group': user_group, 'customer': customer,
               'cart': cart, 'product_total': round(product_total, 2), 'store_item': store_item}
    return render(request, 'account/cart.html', context)

def view_profile(request, user_id, *kwargs):
    customer = Customer.objects.filter(user=request.user)
    volunteer = Volunteer.objects.all()
    photo = Photo.objects.filter(user=request.user)
    vol = None
    for person in volunteer:
        vol = person

    vol_timeslot = Timeslot.objects.filter(volunteer__in=volunteer)
    cus_timeslot = Timeslot.objects.filter(customer__in=customer)

    context = {'user_id': user_id, 'customer': customer, 'volunteer': volunteer,
               'vol_timeslot': vol_timeslot, 'cus_timeslot': cus_timeslot, 'photo': photo}
    return render(request, 'account/profile.html', context)

@login_required
def edit_profile(request):
    user_id=request.user.id
    if request.method == 'POST':
        form = EditCustomerForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user_id)
    else:
        form = EditCustomerForm(instance=request.user)
        context = {'form': form}
        return render(request, 'account/edit_customer.html', context)


@login_required
def change_password(request):
    user_id=request.user.id
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile', user_id=user_id)
        else:
            return redirect('/account/password.html')
    else:
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'account/password.html', context)


@login_required
def add_photo(request, user_id):
    photo_file = request.FILES.get('photo-file', None)
    print(photo_file, 'photo file')
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, user=request.user)
            print(photo, 'volunteer photo')
            photo.save()
        except Exception as e:
            print(e)
            print('An error occurred while uploading a file to S3')
    return redirect('profile', user_id=user_id)




@login_required
def assoc_item(request, user_id, item_id):
    cart = Cart.objects.get(user=request.user).items
    for item in cart.all():
        if item_id == item.id:
            count = item.item_count
            product = item
            product.item_count = count - 1
            product.count_ref += 1
            product.save()
            print(product.count_ref)

    Cart.objects.get(user=request.user).items.add(item_id)
    store_name = Item.objects.get(id=item_id).store.name
    return redirect('detail', store_name=store_name)


@login_required
def disassoc_item(request, user_id, item_id):
    cart = Cart.objects.get(user=request.user).items
    for item in cart.all():
        if item_id == item.id:
            count = item.item_count
            product = item
            product.item_count = count + 1
            if product.count_ref > 0:
                product.count_ref -= 1
            product.save()
            print(product.count_ref)
            if product.count_ref <= 0:
                cart = Cart.objects.get(
                    user=request.user).items.remove(item_id)
    return redirect('cart', user_id=user_id)

