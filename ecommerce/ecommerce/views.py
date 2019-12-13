
from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .forms import ContactForm


def home_page(request):
    args = {

    }
    # check if user is authenticated
    if request.user.is_authenticated():
        args["premium_content"] = "Only shown if the user is logged in and authenticated"


    return render(request,"index.html",args)


def contact_page(request):
    # initialize the contact form and pass data from request
    contact_form = ContactForm(request.POST or None)
    args = {
        "form": contact_form
    }

    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for contacting us"})
 
    # send errors to the page
    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors,status=400,content_type='application/json')

    return render(request,"contact/view.html",args)
