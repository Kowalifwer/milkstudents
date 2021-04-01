from milk_app.models import Listing
from django.shortcuts import render
from django.http import HttpResponse
# from rango.models import Category
# from rango.models import Page
from milk_app.forms import ListingForm, UserForm, UserProfileForm
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
        role = request.POST.get('account')

        if user_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['password_confirm'] and profile_form.is_valid():
            # print(role)
            
            if role == "TNT":
                print("TENANT TEST")
                pass

            elif role == "HST":
                print("HOST TEST")
                pass
            
            
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        elif user_form.cleaned_data['password'] != user_form.cleaned_data['password_confirm']:
             user_form.add_error('password_confirm', 'The passwords do not match')
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'milk_app/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('milk_app:home'))
            else:
                return HttpResponse("Your MilkStudents account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'milk_app/login.html')

def show_listing(request, listing_id_slug):
    context_dict = {}

    try:
        listing = Listing.objects.get(slug = listing_id_slug)

        context_dict['listing'] = listing

    except Listing.DoesNotExist:
        context_dict['listing'] = None
        
    return render(request, 'milk_app/listing.html', context = context_dict)

@login_required
def add_listing(request):
    form = ListingForm()

    if request.method == 'POST':
        form = ListingForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('milk_app:home'))
        else:
            print(form.errors)

    return render(request, 'milk_app/add_listing.html', {'form': form})


def goto_url(request):
    if request.method == 'GET':
        page_id = request.GET.get('page_id')
        try:
            selected_page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('milk_app:home'))
        selected_page.views = selected_page.views + 1
        selected_page.save()
        
        return redirect(selected_page.url)
    return redirect(reverse('milk_app:home'))



@login_required
def user_logout(request):
    logout(request)

    return redirect(reverse('milk_app:home'))

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('milk_app:home'))
    else:
        print(form.errors)
    context_dict = {'form': form}
    return render(request, 'milk_app/profile_registration.html', context_dict)

