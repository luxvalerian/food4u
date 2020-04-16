from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    unit_price = models.IntegerField()
    image = models.CharField(max_length=1000)

    def __str__(self):
        # return data will need to be the item they selceted from the store not self.name
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    # timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)

    def __str__(self):
        # return data will need to be a details page of all the items in User's cart not self.name
        return f"{self.user} has {self.items}"
