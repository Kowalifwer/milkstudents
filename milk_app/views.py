from django.shortcuts import render
from django.http import HttpResponse
# from rango.models import Category
# from rango.models import Page
from milk_app.forms import UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
# Homepage for starters - nothing interesting
def home(request):

    

    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context_dict['pages'] = page_list

    # visitor_cookie_handler(request)
    return render(request, 'milk_app/home.html', context=context_dict)

def about(request):
    
    context_dict = {}
    # visitor_cookie_handler(request)
    # context_dict['visits'] = request.session['visits']
    
    response = render(request, 'milk_app/about.html',context = context_dict)
    return response

def contactPage(request):
    context_dict = {}
    response = render(request, 'milk_app/contact_us.html',context = context_dict)
    return response

def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user


            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:

            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'milk_app/register.html', context = {'user_form' : user_form, 'profile_form' : profile_form, 'registered':registered})