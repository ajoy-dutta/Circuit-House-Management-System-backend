# Generated by Django 5.1.4 on 2024-12-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_rename_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('NDC', 'NDC'), ('Staff', 'Staff')], default='Staff', max_length=10, null=True),
        ),
    ]