from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import AbstractUser

UNITS = (
  ('E', 'Each'),
  ('L', 'LB'),
  ('O', 'OZ'),
  ('F', 'FL OZ'),
  ('U', 'Unit'),
  ('G', 'Gram'),
  ('K', 'KG'),
  ('M', 'GL'),
  ('D', 'Dozen')
)

TIMESLOTS = (
  ("A",	"9AM–10AM"),
  ("B",	"10AM–11AM"),
  ("C",	"11AM–12PM"),
  ("D",	"12PM–1PM"),
  ("E",	"1PM–2PM"),
  ("F",	"2PM–3PM"),
  ("G",	"3PM–4PM"),
  ("H",	"4PM–5PM"),
  ("I",	"5PM–6PM"),
  ("J",	"6PM–7PM"),
  ("K",	"7PM–8PM"),
  ("L",	"8PM–9PM"),
  ("M",	"9PM–10PM")
)

# Extending the User Model
class User(AbstractUser):
  is_customer=models.BooleanField(default=False)
  is_volunteer=models.BooleanField(default=False)


#Volunteer Model
# class Volunteer(models.Model):
#   user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#   is_volunteer=models.BooleanField(default=True)

#   def __str__(self):
#     return f"{self.name}"

#Customer Model
class Customer(models.Model):
  name = models.CharField(max_length=250)
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  is_customer=models.BooleanField(default=True)

  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name}"

#Timeslot Model
class Timeslot(models.Model):
  date = models.DateField()
  timeslot = models.CharField(
    verbose_name="Timeslot",
    max_length=1,
    choices=TIMESLOTS,
    default=TIMESLOTS[0][0])
  volunteer = models.ForeignKey(User, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

  def __str__(self):  
    return f"{self.date} - {self.get_timeslot_display()}"

class Item(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  unit_price = models.FloatField("Price")
  unit_measurement = models.CharField(
    verbose_name="Measurement Units",
    max_length=1,
    choices=UNITS,
    default=UNITS[0][0])
  image = models.CharField(verbose_name="Image URL", max_length=1000)
  
        # return data will need to be the item they selceted from the store not self.name
  def __str__(self):
    return f"{self.name} at ${self.unit_price}/{self.get_unit_measurement_display()}"

class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # checkout_number = Volunteer.objects.count()
    items = models.ManyToManyField(Item)
    # timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)

    def __str__(self):
        # return data will need to be a details page of all the items in User's cart not self.name
        if self.items.count() == 1:
          return f"{self.user}'s' cart has {self.items.count()} item"
        else:
          return f"{self.user}'s' cart has {self.items.count()} items"