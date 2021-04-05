from milk_app.models import Listing, UserProfile
from django.shortcuts import render
from django.http import HttpResponse
from milk_app.forms import ListingForm, UpdateListingForm, UserForm, UserProfileForm, UserProfileUpdateForm, UserUpdateForm, LoginForm
from django.shortcuts import redirect
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import uuid
from django.contrib import messages

domains = [".edu",".ac.uk",".ac.nz", ".student","@student"] 
# Create your views here.
# Homepage for starters - nothing interesting
def home(request):

    context_dict = {}

    return render(request, 'milk_app/home.html', context=context_dict)

def about(request):
    
    context_dict = {}
    
    response = render(request, 'milk_app/about.html',context = context_dict)
    return response

def contactPage(request):
    context_dict = {}
    response = render(request, 'milk_app/contact_us.html',context = context_dict)
    return response
def careers(request):
    context_dict = {}
    response = render(request, 'milk_app/careers.html',context = context_dict)
    return response
def faq (request):
    context_dict = {}
    response = render(request, 'milk_app/FAQ.html',context = context_dict)
    return response

def register(request):
    registered = False
    

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        role = profile_form['account'].value()
        email = user_form['email'].value()
           
        ##CHECK FOR UNI EMAIL DOMAIN
        if role == "Tenant" and not any(x in email for x in domains):                
            user_form.add_error('email', 'Please enter a valid University email address')

        elif user_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['password_confirm'] and profile_form.is_valid():
            
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()
            registered = True
            login(request,user)
            messages.success(request, 'Registration Succesful!')
            return redirect(reverse('milk_app:home'))

        elif user_form.cleaned_data['password'] != user_form.cleaned_data['password_confirm']:
             user_form.add_error('password_confirm', 'The passwords do not match - please enter 2 matching passwords')
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'milk_app/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    context_dict = {}
    login_form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        username = login_form['username'].value()
        password = login_form['password'].value()

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Login succesful!')
            return redirect(reverse('milk_app:home'))
        else:
            login_form.add_error(None, "Incorrect details provided - Please try again")
    
        print(login_form.errors)
    
    return render(request, 'milk_app/login.html', {"login_form" : login_form})

def show_listing(request, listing_id_slug):
    update_form = UpdateListingForm()

    context_dict = {}

    try:
        #listing object reference
        listing = Listing.objects.get(slug = listing_id_slug)

        ### UPDATE LISTING CODE ###
        if request.method == 'POST':
            update_form = UpdateListingForm(request.POST, request.FILES, instance = listing)

        if update_form.is_valid():
            #push update to database
            update_form.save(commit=True)
            
        else:
            update_form = UpdateListingForm(instance = listing)
            
            print(update_form.errors)
    
        owner = listing.user #pass owner data into context dict

        context_dict['listing'] = listing
        context_dict['owner_info'] = owner
        context_dict['updated_listing'] = update_form

    except Listing.DoesNotExist:
        context_dict['listing'] = None
   
    

    if request.user.is_authenticated: #if current user is authenticated - send in their role to context dict.
        context_dict['current_user'] = request.user.userprofile

    return render(request, 'milk_app/listing.html', context = context_dict)



@login_required
def purchase_listing(request, listing_id_slug): #know for a fact its tenant
    
    buyer = request.user.userprofile

    listing = Listing.objects.get(slug = listing_id_slug)
    #update the owner of the listing 
    listing.user = buyer
    #update date
    listing.date = datetime.datetime.now()
    listing.save()

    return redirect(reverse('milk_app:my_listings'))

@login_required
def remove_listing(request, listing_id_slug): #know for a fact its tenant
    #Delete the object from db completely
    Listing.objects.filter(slug = listing_id_slug).delete()

    return redirect(reverse('milk_app:my_listings'))

@login_required
def add_listing(request):
    form = ListingForm()

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            
            listing = form.save(commit=False)
            listing.user = request.user.userprofile
            #Generate
            listing.listing_id = uuid.uuid4().hex
            listing.save()

            return redirect(reverse('milk_app:my_listings'))
        else:
            print(form.errors)

    return render(request, 'milk_app/add_listing.html', {'listing_form': form})


def browse_listings(request):
    context_dict = {}
    listings = Listing.objects.filter(user__account = "Host")

    if request.method == 'POST': #if user searching for smthn
        try:
            search = request.POST.get('search')
            listings = listings.filter(university__icontains = search)
            context_dict['search'] = search
            context_dict['searched'] = True   
        except:
            context_dict['searched'] = False
        
    ##Only Tenants listings should be visible
    
    context_dict['listings'] =listings
    
    return render(request, 'milk_app/browse_listings.html', context_dict)

@login_required
def my_listings(request):
    #request.user.userprofile

    user_p = request.user.userprofile
    
    context_dict = {}
    my_listings = Listing.objects.filter(user = user_p)

    context_dict['my_listings'] = my_listings
    context_dict['profile'] = user_p

    return render(request, 'milk_app/my_listings.html', context_dict)

@login_required
def user_profile(request):
    context_dict = {}
    user = request.user
    user_profile = request.user.userprofile

    p_form = UserProfileUpdateForm()
    u_form = UserUpdateForm()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = user)
        p_form = UserProfileUpdateForm(request.POST,request.FILES, instance = user_profile)

    if p_form.is_valid() and u_form.is_valid():
        u_form.save(commit = True)
        p_form.save(commit = True)
        return redirect(reverse('milk_app:profile'))
    
    else:
        
        u_form = UserUpdateForm(instance=user)
        p_form = UserProfileUpdateForm(instance=user_profile)
        print(p_form.errors, u_form.errors)
    
    context_dict['p_form'] = p_form
    context_dict['u_form'] = u_form


    response = render(request, 'milk_app/profile.html',context = context_dict)
    return response

@login_required
def user_logout(request):
    logout(request)

    messages.success(request, 'Logged out Succesfully!')

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