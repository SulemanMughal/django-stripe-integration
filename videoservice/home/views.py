from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
from django.contrib.auth.models import User

from .models import *

def index(request):
    template_name = "home/index.html"
    courses = Course.objects.all()
    context = {
        "courses" : courses
    }
    return render(request, template_name, context)



def details(request,slug):
    template_name = "home/details.html"
    course = Course.objects.filter(slug=slug).first()
    course_module = CourseModule.objects.filter(course = course)
    context = {
        "course" : course,
        "course_module" : course_module
    }
    return render(request, template_name, context)


def charge(request):
    template_name = "home/charge.html"
    context = {
    
    }
    return render(request, template_name, context)


import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

def BecomePro(request):
    template_name = "home/BecomePro.html"
    if request.method == "POST":
        print(request.POST)
        membershp = request.POST.get("memebership", "MONTHLY")
        amount = 1000
        if membershp == "YEARLY":
            amount = 11000
        stripe.api_key=settings.SECRET_KEY

        customer = stripe.Customer.create(
            email = "test@gmail.com",
            source = request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer = customer,
            amount = amount * 100,
            currency = "inr",
            description = "membership"
        )

        if charge["paid"] == True:
            profile = ProfileUser.objects.filter(user = User.objects.get(id = request.user.id)).first()
            if charge["amount"] == 100000:
                profile.subscription_type = "M"
                profile.is_pro = True
                expiry = datetime.now() + timedelta(30)
                profile.pro_expiry_date = expiry
                profile.save()
            elif charge["amount"] == 100000:
                profile.subscription_type = "Y"
                profile.is_pro = True
                expiry = datetime.now() + timedelta(365)
                profile.pro_expiry_date = expiry
                profile.save()
            else:
                profile.subscription_type = "M"
                profile.is_pro = True
                expiry = datetime.now() + timedelta(30)
                profile.pro_expiry_date = expiry
                profile.save()
            return redirect(reverse("charge"))

    context = {
    
    }
    return render(request, template_name, context)


import json
def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


from django.http import JsonResponse

@csrf_exempt
def create_payment(request):
    try:
        data = json.loads(request.data)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd'
        )

        return JsonResponse({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return JsonResponse({
            "error" : "error"
        })
