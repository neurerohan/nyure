# Generated by Django 5.1.6 on 2025-03-03 09:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vegetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_nepali', models.CharField(blank=True, max_length=100, null=True)),
                ('unit', models.CharField(max_length=20)),
                ('min_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('avg_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('scrape_date', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-scrape_date', 'name'],
                'unique_together': {('name', 'scrape_date')},
            },
        ),
    ]
