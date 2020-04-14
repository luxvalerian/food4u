from django.shortcuts import render, redirect

from . scrapper import produce_dict, logo_img, logo_svg


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def stores(request):
    context = {'product': produce_dict, 'logo': logo_img, 'logo_svg': logo_svg}
    return render(request, 'stores/index.html', context)


def logout(request):
    return HttpResponse('Logged Out')


def stores_index(request):
    return render(request, 'stores/index.html')


def stores_detail(request):
    return render(request, 'stores/detail.html')


def login(request):
    return render(request, 'registration/login.html')


def signup(request):
    return render(request, 'registration/signup.html')
