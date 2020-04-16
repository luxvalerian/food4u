from django.contrib import admin
from .models import Item, Cart, Volunteer

admin.site.register(Volunteer)
admin.site.register(Item)
admin.site.register(Cart)