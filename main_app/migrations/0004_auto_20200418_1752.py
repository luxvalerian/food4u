# Generated by Django 3.0.4 on 2020-04-18 17:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0003_auto_20200418_0612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='volunteer',
        ),
        migrations.AddField(
            model_name='timeslot',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
