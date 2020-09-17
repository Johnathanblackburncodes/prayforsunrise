from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import uuid
import boto3 #added for AWS pic SVL
from .models import Profile #added for AWS pic SVL
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import GameForm
from .models import Game, Hand

#Needed for AWS SVL
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'prayforsunrise'

# Create your views here.


def home(request):
    return render(request, 'home.html')

def room(request, room_name):
    # try:
    game = Game.objects.get(room=room_name)
    room_user = User.objects.get(pk=request.user.id)
    game.user.add(room_user)
    # except:
    #     print(game)
    #     return redirect('/')
    return render(request, 'game/room.html', {
        'room_name': room_name
    })

#added to create a place for photos and bios to live. 
def profile(request, room_name):
    return render(request, 'profile.html')


def add_game(request ):
  form = GameForm(request.POST)
  # validate the form
  new_room = ''
  if form.is_valid():
    # don't save the form to the db until it
    # has the host_id assigned
    new_game = form.save(commit=False)
    try:
        new_game.room = uuid.uuid4().hex[:4]
        new_game.host_id = request.user.id
        new_game.save()
        new_room = 'rooms/' + new_game.room
    except:
        print('An Error has occured generating your room')
    
  else:
      print(f'{form}')
  return redirect(new_room)

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