from collections import namedtuple
from typing import Optional
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid
import os
import datetime


def generate_filename_userpic(instance, filename):
    part = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4().hex, part)
    return os.path.join('profile_images', filename)

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to=generate_filename_userpic, blank=True)
    account = models.CharField(   max_length = 6, 
                                  choices = [(None,""), ("Host","Host"),("Tenant","Tenant")],
                                  help_text= "Note: You must provide a valid Student email to Register as a Tenant",
                                  blank=False)

    
    def __str__(self):
        return self.user.username

def generate_filename_listingpic(instance, filename):
    part = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4().hex, part)
    return os.path.join('listing_images', filename)


class Listing(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name= "userName") #reference to user object
    ##Keep track of who purchased listing or cancelled their lease
    userPrev = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null= True, blank = True, related_name= "userNamePrev" ) #reference to user object


    listing_id = models.UUIDField(primary_key=True)
    
    name = models.CharField(max_length = 40)
    description = models.CharField(max_length= 500)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    address = models.CharField(max_length = 100)

    ##Rating fields
    ratingTotal = models.IntegerField(default = 0)
    ratingCount = models.IntegerField(default = 0)
    ratingCurrent = models.DecimalField(default = 0.00, decimal_places= 2, max_digits= 4)
    ###

    picture = models.ImageField(upload_to = generate_filename_listingpic, blank = False)  
    
    date = models.DateField(default = datetime.date.today, editable = True)
    university = models.CharField(max_length= 40)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.listing_id)
        super(Listing, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Listings'

    def __str__(self):
        return self.name

