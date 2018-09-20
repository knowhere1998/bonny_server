# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-19 19:24
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Baby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('tag', models.CharField(max_length=20, unique=True)),
                ('place_of_birth', models.CharField(max_length=120, verbose_name='Place of Birth')),
                ('weight', models.PositiveIntegerField(default=10)),
                ('blood_group', models.CharField(choices=[(b'a_positive', b'A Positive'), (b'a_negative', b'A Negative'), (b'b_positive', b'B Positive'), (b'b_negative', b'B Negative'), (b'o_positive', b'O Positive'), (b'o_negative', b'O Negative'), (b'ab_positive', b'AB Positive'), (b'ab_negative', b'AB Negative')], max_length=10, verbose_name='gender')),
                ('gender', models.CharField(choices=[(b'male', b'Male'), (b'female', b'Female')], max_length=10, verbose_name='gender')),
                ('birth_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Birth Date')),
                ('special_notes', models.CharField(help_text='Any Medical conditions such as allergies are to be mentioned here', max_length=400, verbose_name='Special Notes')),
                ('text_notifications', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'baby',
                'verbose_name_plural': 'babies',
            },
        ),
        migrations.CreateModel(
            name='Clinitian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(help_text='Please use the following format: <em>+91__________</em>.', max_length=128)),
                ('unique_id', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 12', regex='^.{12}$')], verbose_name='Aadhaar ID')),
                ('user', models.OneToOneField(help_text='Create a new user to add as a  Clinitian. This would be used as login credentials.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Clinitian',
                'verbose_name_plural': 'Clinitians',
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('address', models.CharField(max_length=200)),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(help_text='Please use the following format: <em>+91__________</em>.', max_length=128)),
                ('unique_id', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 12', regex='^.{12}$')], verbose_name='Aadhaar ID')),
                ('user', models.OneToOneField(help_text='Create a new user to add as a Parent or Guardian. This would be used as login credentials.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'parent',
                'verbose_name_plural': 'parents',
            },
        ),
        migrations.CreateModel(
            name='VaccineRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine', models.CharField(choices=[(0, ((b'bcg', b'BCG'), (b'opv', b'OPV0'), (b'hepb1', b'HEP-B 1'))), (6, ((b'dt1', b'DTwP 1'), (b'ipv1', b'IPV 1'), (b'hepb2', b'HEP-B 2'), (b'hib1', b'HIB 1'), (b'rota1', b'Rotavirus 1'), (b'pcv1', b'PCV 1'))), (10, ((b'dt2', b'DTwP 2'), (b'ipv2', b'IPV 2'), (b'hib2', b'HIB 2'), (b'rota2', b'Rotavirus 2'), (b'pcv2', b'PCV 2'))), (14, ((b'dt3', b'DTwP 3'), (b'ipv3', b'IPV 3'), (b'hib3', b'HIB 3'), (b'rota3', b'Rotavirus 3'), (b'pcv3', b'PCV 3'))), (24, ((b'opv1', b'OPV 1'), (b'hepb3', b'HEP-B 3'))), (36, ((b'opv2', b'OPV 2'), (b'mmr1', b'MMR-1')))], max_length=20, verbose_name='Vaccine')),
                ('administered_on', models.DateField(default=datetime.datetime.now)),
                ('administered_at', models.DateField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[(b'pending', b'Pending'), (b'scheduled', b'Scheduled'), (b'administered', b'Administered')], max_length=20, verbose_name='Vaccine Status')),
                ('baby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccine_records', to='operations.Baby')),
            ],
        ),
        migrations.CreateModel(
            name='VaccineSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine', models.CharField(choices=[(0, ((b'bcg', b'BCG'), (b'opv', b'OPV0'), (b'hepb1', b'HEP-B 1'))), (6, ((b'dt1', b'DTwP 1'), (b'ipv1', b'IPV 1'), (b'hepb2', b'HEP-B 2'), (b'hib1', b'HIB 1'), (b'rota1', b'Rotavirus 1'), (b'pcv1', b'PCV 1'))), (10, ((b'dt2', b'DTwP 2'), (b'ipv2', b'IPV 2'), (b'hib2', b'HIB 2'), (b'rota2', b'Rotavirus 2'), (b'pcv2', b'PCV 2'))), (14, ((b'dt3', b'DTwP 3'), (b'ipv3', b'IPV 3'), (b'hib3', b'HIB 3'), (b'rota3', b'Rotavirus 3'), (b'pcv3', b'PCV 3'))), (24, ((b'opv1', b'OPV 1'), (b'hepb3', b'HEP-B 3'))), (36, ((b'opv2', b'OPV 2'), (b'mmr1', b'MMR-1')))], max_length=20, verbose_name='Vaccine')),
                ('week', models.PositiveIntegerField(default=0)),
                ('tentative_date', models.DateField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[(b'pending', b'Pending'), (b'scheduled', b'Scheduled'), (b'administered', b'Administered')], max_length=20, verbose_name='Vaccine Status')),
                ('baby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccine_schedules', to='operations.Baby')),
            ],
        ),
        migrations.AddField(
            model_name='baby',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baby', to='operations.Parent'),
        ),
    ]
