# Generated by Django 2.1.2 on 2018-12-28 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proprietaire', '__first__'),
        ('countries_plus', '0005_auto_20160224_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='Immeuble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=512, null=True)),
                ('adresse', models.CharField(max_length=512, null=True)),
                ('jour_emission_facture', models.IntegerField(default=5)),
                ('jour_valeur_facture', models.IntegerField(default=5)),
                ('ville', models.CharField(max_length=128, null=True)),
                ('quartier', models.CharField(max_length=128, null=True)),
                ('longitude', models.DecimalField(decimal_places=12, max_digits=20)),
                ('latitude', models.DecimalField(decimal_places=12, max_digits=20)),
                ('ref_immeuble', models.CharField(max_length=50, null=True)),
                ('pays', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='countries_plus.Country')),
                ('proprietaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proprietaire.Proprietaire')),
            ],
            options={
                'verbose_name': 'Immeuble',
                'verbose_name_plural': 'Immeubles',
            },
        ),
    ]
