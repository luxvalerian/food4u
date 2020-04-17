from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .scraper import produce_dict, logo_img, logo_svg
from .models import Item, Cart, Customer, User, Timeslot #,Volunteer
from .forms import CustomerSignUpForm, VolunteerSignUpForm


# class CustomerSignUpView(CreateView):
#     model = User
#     form_class = CustomerSignUpForm
#     template_name = 'registration/signup_form.html'

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'customer'
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('stores')


def customer_signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaded_data.get('username')
            password = form.cleaded_data.get('password1')
            # email= form.cleaded_data.get('email')
            # first_name = form.cleaded_data.get('first_name')
            # last_name = form.cleaded_data.get('last_name')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('stores')
        else:
            error_message = 'Invalid sign up - try again'
    form = CustomerSignUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup_form.html', context)



class VolunteerSignUpView(CreateView):
    model = User
    form_class = VolunteerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'volunteer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('')

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
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


def remove_vol(request):
    # Timeslot.objects.get(id=timeslot_id).volunteers.remove(volunteer_id)
    
    return redirect('customer/index.html')

@login_required
def checkout(request): #volunteer_id
    # volunteer = Volunteer.objects.get(id=volunteer_id)
    # customer = Customer.objects.get(id=customer_id)
    # timeslot = Customer.objects.get(id=timeslot_id)
    # cart = Cart.objects.get(id=cart_id)
    
    # context = { "customer": customer, "timeslot": timeslot, "cart": cart}#"volunteer": volunteer
    return render(request, 'checkout.html')

def customer_index(request):
    # customer = Customer.objects.get(id=customer_id)

    context = {'customer': customer}
    return render(request, 'customer/index.html')

@login_required
def cart(request):
    return render(request, 'cart/cart.html')