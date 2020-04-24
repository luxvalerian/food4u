from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import Group
from django.urls import reverse
from datetime import date
from . forms import CustomerSignUpForm, VolunteerSignUpForm
from .models import Item, Cart, Timeslot, Customer, Volunteer, User, Store
from .decorators import allowed_users
# from .scraper import produce_dict


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
    customer = Customer.objects.filter(user=request.user).first()
    volunteer = Volunteer.objects.filter(user=request.user).first()
    vol_timeslot = Timeslot.objects.filter(volunteer=volunteer)
    cus_timeslot = Timeslot.objects.filter(customer=customer)

    context = {'customer': customer, 'volunteer': volunteer,
               'vol_timeslot': vol_timeslot, 'cus_timeslot': cus_timeslot}
    return render(request, 'account/profile.html', context)

@login_required
def stores_index(request):
    stores = Store.objects.all()
    context = { 'stores': stores}
    return render(request, 'stores/index.html', context)


@login_required
def stores_detail(request, store_name):
    stores = Store.objects.all()
    store = stores.filter(name=store_name).first()
    items = Item.objects.filter(store=store)
    context = {'items': items, 'store': store}
    return render(request, 'stores/detail.html', context)


def logout(request):
    return render(request, 'home.html')


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
    # timeslot = Timeslot.objects.filter(customer=customer)
    # timeslot_count = timeslot.count()
    cart = Cart.objects.filter(user=request.user).all()
    # items_not_in_cart = Item.objects.exclude(id__in = cart.items.all().values_list('id'))
    print(cart.all())
    user_group = str(request.user.groups.all()[0])
    product_total = 0
    for obj in cart:
        for product in obj.items.all():
            item = Item.objects.filter(id=product.id)
            piece = item.first()
            print(piece)
            product_total += piece.unit_price
            print(product_total)

            # product_price = (product.price * 2)
    context = {'user_group': user_group, 'customer': customer,
               'cart': cart, 'product_total': round(product_total, 2)}
    return render(request, 'account/cart.html', context)


class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerSignUpForm
    # fields =  ['delivery_time']

    def get_object(self, *args, **kwargs):
        user = self.request.user

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user

    def get_success_url(self, *args, **kwargs):
        return reverse("profile")


class VolunteerUpdate(LoginRequiredMixin, UpdateView):
    model = Volunteer
    form_class = VolunteerSignUpForm
#   fields =  ['availability_date', 'availability']

    def get_object(self, *args, **kwargs):
        user = self.request.user

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user

    def get_success_url(self, *args, **kwargs):
        return reverse("profile")
