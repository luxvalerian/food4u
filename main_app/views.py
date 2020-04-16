from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from . scraper import produce_dict, logo_img, logo_svg

num_of_volunteer = 5
num_of_checkouts = 0


def remove_vol(request):
    total_volunteers = num_of_volunteer - 1
    total_checkouts = num_of_checkouts + 1
    return redirect('checkout', total_volunteers, total_checkouts)


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

def checkout(request, total_volunteers, total_checkouts):
    num_of_volunteer = total_volunteers
    num_of_checkouts = total_checkouts
    context = {"volunteer": num_of_volunteer, "customer": num_of_checkouts}
    return render(request, 'checkout.html', context)
