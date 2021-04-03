from django import forms
from milk_app.models import Listing, UserProfile
from django.contrib.auth.models import User
import datetime

# class CategoryForm(forms.ModelForm):
#     name = forms.CharField(max_length = Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
#     likes = forms.IntegerField(widget = forms.HiddenInput(), initial= 0)
#     slug = forms.CharField(widget = forms.HiddenInput(), required = False)

#     class Meta:
#         model = Category
#         fields = ('name', )
    
# class PageForm(forms.ModelForm):
#     title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
#     url = forms.URLField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the URL of the page.")
#     views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

#     class Meta:
#         model = Page
#         exclude = ('category', )

#     def clean(self):
#         cleaned_data = self.cleaned_data
#         url = cleaned_data.get('url')

#         if url and not url.startswith('http://'):
#             url = f'http://{url}'
#             cleaned_data['url'] = url

#         return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    password_confirm = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('picture','account' )        

class ListingForm(forms.ModelForm):

    
    name = forms.CharField(max_length = 40, help_text= "Name your listing")
    description = forms.CharField(max_length= 500, help_text = "Describe your listing")
    price = forms.IntegerField(widget=forms.HiddenInput(),required = False)
    address = forms.CharField(max_length = 100, help_text = "Address")
    rating = forms.IntegerField(widget=forms.HiddenInput(), required = False)
    date = forms.DateField(widget=forms.HiddenInput(), initial = datetime.date.today())
    uniName = forms.CharField(max_length= 40, initial = "University of Glasgow", help_text="name of uni")
    
    picture = forms.ImageField(required = False, help_text = "Image of Property")
    
    
    slug = forms.SlugField(widget=forms.HiddenInput(), required = False)

    class Meta:
        model = Listing
        fields = ('name','description','address','uniName','picture')
        exclude = ('user', 'rating', 'date', 'price', 'listing_id')
