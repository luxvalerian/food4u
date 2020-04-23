from django.http import HttpResponse
from .models import Item, Cart, Timeslot
from django.shortcuts import redirect


def allowed_users(allowed_roles=[]):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
      group = None
      if request.user.groups.exists():
        group = request.user.groups.all()[0].name

      if group in allowed_roles:
        # print('Working', allowed_roles, group)
        return view_func(request, *args, **kwargs)
      else:
        # print('Working', allowed_roles, group)
        return HttpResponse('You are not authorized')
    return wrapper_func
  return decorator
