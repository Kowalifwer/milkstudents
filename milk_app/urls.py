from django.urls import path
from milk_app import views


##CHANGE IT UP - IMPORTANT TO HAVE REFERENCES FOR URLS.
app_name = 'milk_app'



urlpatterns = [
    
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('support/contact_us/', views.contactPage, name = 'contact'),
    path('listing/<slug:listing_id_slug>', views.show_listing, name="show_listing"),
    path('add_listing/', views.add_listing, name='add_listing'),
    path('browse_listings/', views.browse_listings, name = 'browse_listings'),
    path('my_listings/', views.my_listings, name = "my_listings"),
    path('FAQ/', views.faq, name = "FAQ"),
    path('careers/', views.careers, name = "careers"),
    path('purchase/<slug:listing_id_slug>', views.purchase_listing, name = "purchase_listing"),
    path('remove/<slug:listing_id_slug>', views.remove_listing, name = "remove_listing"),
    path('rate/<slug:listing_id_slug>', views.rate_listing, name = "rate_listing"),
    path('cancel/<slug:listing_id_slug>', views.cancel_listing, name = "cancel_listing"),

    path ('profile/', views.user_profile, name = "profile"),

    #Registration
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register' ),
    path('login/', views.user_login, name='login'),
]