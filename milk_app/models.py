from collections import namedtuple
from typing import Optional
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid
import os
import datetime
# Create your models here.
# class Category(models.Model):
#     NAME_MAX_LENGTH = 128


#     name = models.CharField(max_length= NAME_MAX_LENGTH, unique=True)
#     views = models.IntegerField(default = 0)
#     likes = models.IntegerField(default = 0)
#     slug = models.SlugField(unique = True)

#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(Category, self).save(*args, **kwargs)

#     class Meta:
#         verbose_name_plural = 'Categories'

#     def __str__(self):
#         return self.name

# class Page(models.Model):
#     TITLE_MAX_LENGTH = 128
#     URL_MAX_LENGTH = 200
    
#     category = models.ForeignKey(Category, on_delete = models.CASCADE)
#     title= models.CharField(max_length=TITLE_MAX_LENGTH)
#     url = models.URLField()
#     views = models.IntegerField(default = 0)

#     def __str__(self):
#         return self.title

def generate_filename_userpic(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4().hex, ext)
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





def generate_filename_listing(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4().hex, ext)
    return os.path.join('listing_images', filename)


class Listing(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE) #reference to user object
    

    listing_id = models.UUIDField(primary_key=True)
    
    name = models.CharField(max_length = 40)
    description = models.CharField(max_length= 500)
    price = models.IntegerField(null=True)
    address = models.CharField(max_length = 100)

    ##Rating fields
    ratingTotal = models.IntegerField(default = 0)
    ratingCount = models.IntegerField(default = 0)
    ratingCurrent = models.DecimalField(default = 0.00, decimal_places= 2, max_digits= 4)
    ###

    picture = models.ImageField(upload_to = generate_filename_listing, blank = False)
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

