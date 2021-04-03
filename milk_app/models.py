from collections import namedtuple
from typing import Optional
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

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

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    account = models.CharField(   max_length = 6, 
                                  choices = [(None,""), ("Host","Host"),("Tenant","Tenant")],
                                  help_text= "What kind of account is this?",
                                  blank=False)
    def __str__(self):
        return self.user.username


class Listing(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE) #reference to user object
    
    listing_id = models.CharField(max_length = 32, primary_key= True)
    name = models.CharField(max_length = 40)
    description = models.CharField(max_length= 500)
    price = models.IntegerField(null=True)
    address = models.CharField(max_length = 100)
    rating = models.IntegerField(null=True)
    picture = models.ImageField(upload_to = 'listing_images', blank = True)
    date = models.DateField(null=True)
    uniName = models.CharField(max_length= 40)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.listing_id)
        super(Listing, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Listings'

    def __str__(self):
        return self.name


