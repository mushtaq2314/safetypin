from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path("",views.index,name='home'),
path("index.html",views.index,name='home'),
# path("about",views.about,name='about'),
path("login.html",views.Login,name='login'),
path("generate.html",views.generate,name='generate'),
path("signup.html",views.signup,name='signup'),
path("forgot.html",views.forgot,name='forgot'),
path("home.html",views.home,name='home'),
path("contact.html",views.contact,name="contact"),
path("services.html",views.services,name="sevices"),
path("profile.html",views.profile,name="profile"),
path("store.html",views.store,name="store"),
path("help.html",views.help,name="help"),
path("passwords.html",views.passwords,name="passwords"),
path("wallet.html",views.wallet,name="wallet"),
]
