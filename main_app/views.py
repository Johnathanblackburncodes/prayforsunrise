from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import uuid
import boto3 #added for AWS pic SVL
from .models import Profile #added for AWS pic SVL

#Needed for AWS SVL
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'prayforsunrise'

# Create your views here.


def home(request):
    return render(request, 'home.html')

def room(request, room_name):
    return render(request, 'game/room.html', {
        'room_name': room_name
    })

#added to create a place for photos and bios to live. 
def profile(request, room_name):
    return render(request, 'profile.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def add_photo(request, user_id):
    photo_file = request.FILES.get('photo-file', NONE)

    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Profile(image=url, puser=user_id)
            photo.save()
        except:
            print('Oops, something went wrong. Please try again.')
    return redirect ('registration/signup.html')