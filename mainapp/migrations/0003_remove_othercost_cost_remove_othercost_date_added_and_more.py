# Generated by Django 5.1.4 on 2024-12-23 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_food_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='othercost',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='othercost',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='othercost',
            name='items',
        ),
        migrations.AddField(
            model_name='othercost',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='othercost',
            name='item',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='othercost',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='othercost',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.room'),
        ),
        migrations.AlterField(
            model_name='othercost',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.guest'),
        ),
    ]
