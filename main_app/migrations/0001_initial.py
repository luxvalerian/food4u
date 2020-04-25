
# Generated by Django 3.0.4 on 2020-04-25 17:53


import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


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
                ('item_count', models.IntegerField(null=True)),
                ('count_ref', models.IntegerField(default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100, null=True)),
                ('image', models.CharField(max_length=1000, null=True, verbose_name='Image URL')),
            ],
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('timeslot', models.CharField(choices=[('A', '9AM–10AM'), ('B', '10AM–11AM'), ('C', '11AM–12PM'), ('D', '12PM–1PM'), ('E', '1PM–2PM'), ('F', '2PM–3PM'), ('G', '3PM–4PM'), ('H', '4PM–5PM'), ('I', '5PM–6PM'), ('J', '6PM–7PM'), ('K', '7PM–8PM'), ('L', '8PM–9PM'), ('M', '9PM–10PM')], default='A', max_length=1, verbose_name='Timeslot')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability_date', models.DateField(null=True, verbose_name='available date')),
                ('availability', multiselectfield.db.fields.MultiSelectField(choices=[('A', '9AM–10AM'), ('B', '10AM–11AM'), ('C', '11AM–12PM'), ('D', '12PM–1PM'), ('E', '1PM–2PM'), ('F', '2PM–3PM'), ('G', '3PM–4PM'), ('H', '4PM–5PM'), ('I', '5PM–6PM'), ('J', '6PM–7PM'), ('K', '7PM–8PM'), ('L', '8PM–9PM'), ('M', '9PM–10PM')], max_length=100)),
                ('customer', models.ManyToManyField(through='main_app.Timeslot', to='main_app.Customer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='timeslot',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Volunteer'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Store'),
        ),
        migrations.CreateModel(
            name='CustomerDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('date', models.DateField(verbose_name='Delivery date')),
                ('delivery_time', models.CharField(choices=[('A', '9AM–10AM'), ('B', '10AM–11AM'), ('C', '11AM–12PM'), ('D', '12PM–1PM'), ('E', '1PM–2PM'), ('F', '2PM–3PM'), ('G', '3PM–4PM'), ('H', '4PM–5PM'), ('I', '5PM–6PM'), ('J', '6PM–7PM'), ('K', '7PM–8PM'), ('L', '8PM–9PM'), ('M', '9PM–10PM')], default='A', max_length=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Customer')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('is_ordered', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(to='main_app.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
