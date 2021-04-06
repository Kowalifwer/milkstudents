import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'milkstudents.settings')
import uuid

import django
django.setup()
from django.contrib.auth.models import User
from milk_app.models import UserProfile,Listing

def populate():

        #ALL PASSWORDS ARE 1234 FOR SIMPLICITY

        #Create Host 1 username karen
        new_user = User.objects.create_user(username = "karen", email = "Karen@gmail.com", password = "1234")
        karen_host = UserProfile.objects.create(user = new_user, account = "Host")

        #Create Host 2 username kate
        new_user1 = User.objects.create_user(username = "kate", email = "Kate@gmail.com", password = "1234")
        kate_host = UserProfile.objects.create(user = new_user1, account = "Host")

        #Create Tenant 1 username lincoln
        new_user2 = User.objects.create_user(username = "lincoln", email = "Lincoln@gmail.com", password = "1234")
        lincoln_tnt = UserProfile.objects.get_or_create(user = new_user2, account = "Host")

        #Create Tenant 2 username jake
        new_user3 = User.objects.create_user(username = "jake", email = "Jake@gmail.com", password = "1234")
        jake_tnt = UserProfile.objects.get_or_create(user = new_user3, account = "Host")

        #karents listing 1
        Listing.objects.get_or_create(user = karen_host, listing_id = uuid.uuid4().hex, name = "Cool house", description = "Nice looking house", price = 1452.32, address = "12 Byres Road", university = "Univeristy of Glasgow", picture = "#")

        #karents listing 2
        Listing.objects.get_or_create(user = karen_host, listing_id = uuid.uuid4().hex, name = "Cooler house", description = "Nicer looking house", price = 1852.32, address = "16 Johns Road", university = "Univeristy of Edinburgh", picture = "#")

        #karents listing 3
        Listing.objects.get_or_create(user = karen_host, listing_id = uuid.uuid4().hex, name = "Coolest house", description = "Nicest looking house", price = 2452.82, address = "2 Byres Road", university = "Univeristy of Glasgow", picture = "#")

        #karents listing 4
        Listing.objects.get_or_create(user = karen_host, listing_id = uuid.uuid4().hex, name = "The Coolestest house", description = "Nicectest looking house", price = 2952.12, address = "12 Ant Street", university = "Univeristy of Edinburgh", picture = "#")

        #karents listing 1
        Listing.objects.get_or_create(user = kate_host, listing_id = uuid.uuid4().hex, name = "Funky house", description = "Funky looking house", price = 452.32, address = "122 Son Road", university = "Univeristy of Glasgow", picture = "#")

        #karents listing 1
        Listing.objects.get_or_create(user = kate_host, listing_id = uuid.uuid4().hex, name = "Funkier house", description = "Funkier looking house", price = 852.32, address = "16 Just Road", university = "Univeristy of Sheffield", picture = "#")

        #karents listing 1
        Listing.objects.get_or_create(user = kate_host, listing_id = uuid.uuid4().hex, name = "Funkiest house", description = "Funkiest looking house", price = 452.82, address = "66 Can Road", university = "Univeristy of Coolness", picture = "#")

        #karents listing 1
        Listing.objects.get_or_create(user = kate_host, listing_id = uuid.uuid4().hex, name = "The Funkiestest house", description = "Funkiestest looking house", price = 952.12, address = "11 Ant Street", university = "Univeristy of Strathclyde", picture = "#")

 #Start execution
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
    print('Database populated succesfully!\n you have 4 users: karen,kate,lincoln,jake \n their passwords for login is: 1234...\n unfortunately, pictures cannot be added from the script, as their name gets hashed during object creation, and we cannot fetch them from existing images, only by actually submitting through the form.\n this means picture fields in my listings will be empty, but you can update listing and add an image on the host owner account, that should work')






