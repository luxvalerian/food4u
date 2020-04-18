from django.contrib import admin
from .models import Item, Cart, Customer, Timeslot #,Volunteer

# admin.site.register(Volunteer)
admin.site.register(Customer)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Timeslot)
