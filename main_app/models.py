from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#Volunteer Model Manager
class VolunteerManager(BaseUserManager):
  def create_user(self, email, username, password=None):
    if not email:
      raise ValueError("Users must have an email address")
    if not username:
      raise ValueError("Users must have a username")

    user = self.model(
      email=self.normalize_email(email),
      username=username
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, username, password):
    user = self.create_user(
      email=self.normalize_email(email),
      password=password,
      username=username
    )
    
    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    
    user.save(using=self._db)
    return user

# Volunteer Class
class Volunteer(AbstractBaseUser):
  email=models.EmailField(verbose_name="email", max_length=100, unique=True)
  username=models.CharField(max_length=30, unique=True)
  date_joined=models.DateTimeField(verbose_name='date joined', auto_now_add=True)
  last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
  is_admin=models.BooleanField(default=False)
  is_active=models.BooleanField(default=True)
  is_staff=models.BooleanField(default=False)
  is_superuser=models.BooleanField(default=False)
  is_volunteer=models.BooleanField(default=True)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  objects = VolunteerManager()

  def __str__(self):
    return f"{self.username} joined {self.date_joined}"

  def has_perm(self, perm, obj=None):
    return self.is_admin

  def has_module_perms(self, app_label):
    return True



#Timeslot Model
class Timeslot(models.Model):
  date = models.DateField()
  timeslot = models.TimeField('timeslot')
  volunteer = models.ManyToManyField(Volunteer)

  # volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
  
  #cart = models.ForeignKey()
  #cart = models.ForeignKey()
  #cart = models.ForeignKey()

#Volunteer Model

# class Transactions(models.Model):
#   name = models.DateField()
#   complete = models.?
  #timeslot = models.ForeignKey()
  #volunteer = models.ForeignKey()
  #user = models.ForeignKey()
  #cart = models.ForeignKey()
  #cart = models.ForeignKey()
