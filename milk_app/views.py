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