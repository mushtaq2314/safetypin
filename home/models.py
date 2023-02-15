from django.db import models

# Create your models here.
class SignUP(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    image = models.ImageField(default='img19_1920x1200.jpg',upload_to='downloaded')
    phone = models.IntegerField(default=0)
    gender = models.CharField(max_length=6)
    DOB = models.CharField(max_length=50)
    passwords = models.CharField(max_length=10000000,default="cSNYUmE677m3C77+k6ltnucqkJMZbeOxo2cb74W5xCXBVGOXS2/t5jGxs0aHv216EvPFjXQt76tQ3UWIJjV5vEMn8FpGP43wYEg+2cLdD6PYTldXcBgiw6/UhhUe74RW74Gze9kX4PRxfihu4kZaePxOZXZJLRfZFoQmr6x+N7ir2+kye7v5+s3d2H1PA8F2")

    def __str__(self) -> str:
        return self.name