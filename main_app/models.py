from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

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


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    delivery_time = MultiSelectField(	
        max_length=100, null=True, choices=TIMESLOTS, max_choices=3)
        # MultiSelectField(max_length=100, null=True, choices=TIMESLOTS, max_choices=3)

    def get_absolute_url(self):
        return reverse('checkout', kwargs={'customer_id': self.id})

    def get_absolute_url(self):
        return reverse('profile')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class CustomerDelivery(models.Model):
  date = models.DateField(verbose_name='Delivery date', default=date.today())
  delivery_time = models.CharField(
        max_length=1,
        choices=TIMESLOTS,
        default=TIMESLOTS[0][0]) 
  
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_delivery_time_display()} on {self.date}"

  class Meta:
    ordering = ['date']

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    availability_date = models.DateField(
        verbose_name='available date', null=True)
    availability = MultiSelectField(max_length=100, choices=TIMESLOTS)

    customer = models.ManyToManyField(Customer, through="Timeslot")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Timeslot(models.Model):
    date = models.DateField()
    timeslot = models.CharField(
        verbose_name="Timeslot",
        max_length=1,
        choices=TIMESLOTS,
        default=TIMESLOTS[0][0])

    def __str__(self):
        return f"{self.date} at {self.get_timeslot_display()}"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)


class Store(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100, null=True)
    image = models.CharField(verbose_name="Image URL",
                             max_length=1000, null=True)

    def __str__(self):
        return f"{self.name}"


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
    item_count = models.IntegerField(null=True)
    count_ref = models.IntegerField(default=1, null=True)

    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} at ${self.unit_price}/{self.get_unit_measurement_display()}"

    def line_total(self):
        return (self.count_ref * self.unit_price)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    order_date = models.DateTimeField(auto_now=True)
    is_ordered = models.BooleanField(default=False)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.unit_price for item in self.items.all()])

    def __str__(self):
        if self.items.count() == 1:
            return f"{self.user.first_name}'s cart has {self.items.count()} item"
        else:
            return f"{self.user.first_name}'s cart has {self.items.count()} items"


class Photo(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for user_id: {self.user_id} @{self.url}"


class LineItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(
        decimal_places=2,
        max_digits=6)
