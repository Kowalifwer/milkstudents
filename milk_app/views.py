from milk_app.models import Listing, UserProfile
from django.shortcuts import render
from django.http import HttpResponse
from milk_app.forms import ListingForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from uuid import uuid4 as uuid

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
    domains = [".edu",".ac.uk",".ac.nz"] 

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        role = profile_form['account'].value()
        email = user_form['email'].value()
           
        ##CHECK FOR UNI EMAIL DOMAIN
        if role == "Tenant" and not any(x in email for x in domains):                
            user_form.add_error('email', 'Please enter a valid University email address:')

        elif user_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['password_confirm'] and profile_form.is_valid():
            
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
            login(request,user)
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
    #context_dict['current_user'] = "anon" #anon by default

    try:
        listing = Listing.objects.get(slug = listing_id_slug)
        owner = listing.user #pass owner data into context dict

        context_dict['listing'] = listing
        context_dict['owner_info'] = owner

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
    listing.save()

    return render(request, 'milk_app/home.html')

@login_required
def remove_listing(request, listing_id_slug): #know for a fact its tenant
    #Delete the object from db completely
    Listing.objects.filter(slug = listing_id_slug).delete()

    return render(request, 'milk_app/home.html')




@login_required
def add_listing(request):
    form = ListingForm()


    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            
            listing = form.save(commit=False)
            listing.user = request.user.userprofile
            listing.listing_id = uuid().hex
            listing.picture = request.FILES['picture']

            listing.save() #final save. we generated primary key.

            return redirect(reverse('milk_app:home'))
        else:
            print(form.errors)

    return render(request, 'milk_app/add_listing.html', {'form': form})

def browse_listings(request):
    context_dict = {}
    listings = Listing.objects.filter(user__account = "Host")

    if request.method == 'POST': #if user searching for smthn
        try:
            search = request.POST.get('search')
            listings = listings.filter(uniName__icontains = search)
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
    
    
    response = render(request, 'milk_app/profile.html',context = context_dict)
    return response



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

