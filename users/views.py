# Maintained by: Ian
from django.shortcuts import render, redirect  # To render the template and redirect to another page
from django.contrib import messages  # To send alert messages to the user
from .forms import UserRegisterForm  # To create a custom user registration form
from django.contrib.auth.models import User, Group  # To gain access to the django internal user and group model
import urllib  # To send a request to the google recaptcha api
import urllib.request # To send a request to the google recaptcha api
import Web.settings as settings  # To gain access to the settings of the app
import json  # To parse the response from the google recaptcha api
from .models import PromoCode  # Deprecated in this project
from core.models import Profil  # To create a profile for the new created user -> Database

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            
            # Email is Unique
            email = form.cleaned_data.get("email")
            if result["success"]:
                # Email Verification
                
                # Email is Unique
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Die E-Mail ist schon bei einem anderen Account verwendet worden.")
                    return render(request, "register.html", {'form': form})
                else:
                    form.save()
                    # Get user
                    user = User.objects.get(email=email)
                    
                    Profil.objects.create(user=user)  # Create Profile for the new created user.
                    
                    # activateCode(request, form.cleaned_data.get("promoCode"), user)
                
                messages.success(request, f"Account erfolgreich erstellt!")
                return redirect('login')
            else:
                messages.error(request, "reCaptcha Überprüfung fehlgeschlagen. Versuche es bitte erneut.")
            
    else:
        form = UserRegisterForm()
    try:
        return render(request, "register.html", {'form': form})
    except Exception as e:
        print(e)


def activateCode(request, code, user):
    if code == "":
        return False
    promo = PromoCode.objects.filter(code=code).get()
    if promo:
        data = json.loads(promo.attributes)
        for i in data["groups"]:
            group = Group.objects.filter(name=i).get()
            if group:
                group.user_set.add(user)
        if promo.uses != -1:
            promo.uses -= 1
            if promo.uses == 0:
                promo.delete()
            promo.save()
    else:
        messages.error(request, "Der Eingegebene Promocode ist entweder falsch geschrieben oder nicht existent")
        
