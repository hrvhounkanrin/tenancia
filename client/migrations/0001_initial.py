# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-18 15:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('banque', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode_paiement', models.CharField(blank=True, max_length=64, null=True)),
                ('profession', models.CharField(blank=True, max_length=128, null=True)),
                ('ice_contact', models.CharField(max_length=128, null=True)),
                ('ice_number', models.CharField(max_length=28, null=True)),
                ('ice_relation', models.CharField(blank=True, max_length=64, null=True)),
                ('banque', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='banque.Banque')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]