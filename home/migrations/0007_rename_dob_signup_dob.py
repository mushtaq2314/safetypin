# Generated by Django 4.1.3 on 2022-12-10 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_signup_dob_signup_gender_signup_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signup',
            old_name='dob',
            new_name='DOB',
        ),
    ]
