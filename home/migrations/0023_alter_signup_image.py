# Generated by Django 4.1.3 on 2023-01-14 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_alter_signup_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='image',
            field=models.ImageField(upload_to='downloaded'),
        ),
    ]
