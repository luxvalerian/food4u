# Generated by Django 3.0.4 on 2020-04-18 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_customer', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=250)),
                ('unit_price', models.FloatField(verbose_name='Price')),
                ('unit_measurement', models.CharField(choices=[('E', 'Each'), ('L', 'LB'), ('O', 'OZ'), ('F', 'FL OZ'), ('U', 'Unit'), ('G', 'Gram'), ('K', 'KG'), ('M', 'GL'), ('D', 'Dozen')], default='E', max_length=1, verbose_name='Measurement Units')),
                ('image', models.CharField(max_length=1000, verbose_name='Image URL')),
            ],
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('timeslot', models.CharField(choices=[('A', '9AM–10AM'), ('B', '10AM–11AM'), ('C', '11AM–12PM'), ('D', '12PM–1PM'), ('E', '1PM–2PM'), ('F', '2PM–3PM'), ('G', '3PM–4PM'), ('H', '4PM–5PM'), ('I', '5PM–6PM'), ('J', '6PM–7PM'), ('K', '7PM–8PM'), ('L', '8PM–9PM'), ('M', '9PM–10PM')], default='A', max_length=1, verbose_name='Timeslot')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Customer')),
                ('volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(to='main_app.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Customer')),
            ],
        ),
    ]
