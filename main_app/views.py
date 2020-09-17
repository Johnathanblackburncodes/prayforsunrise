from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import uuid, random
import boto3 #added for AWS pic SVL
from .models import Profile #added for AWS pic SVL

#Needed for AWS SVL
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'prayforsunrise'

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import GameForm, SetupGameForm
from .models import Game, Card, Hand, STAGES

V_STAGES = [t[0] for t in STAGES if t[0]]
# Create your views here.


def home(request):
    return render(request, 'home.html')

def room(request, room_name):
    try:
        game = Game.objects.get(room=room_name)
        room_user = User.objects.get(pk=request.user.id)
        game.user.add(room_user)
    except:
        print(game)
        return redirect('/')
    return render(request, 'game/room.html', {
        'room_name': room_name,
        'game': game
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

def setup_game( request ):
    form = SetupGameForm(request.POST)
    if form.is_valid():
        update_game=form.save(commit=False)
    #None of the above is doing anything but it's a placeholder while we brute force setup
    start_game = Game.objects.get(room=update_game.room)
    
    index_of_stage = V_STAGES.index(start_game.stage)
    #gets the list of users in our game
    players = start_game.user.all()
    
    #lets create a hand for each user in the game.
    for player in players:
        print(f'{player} in {players}')
        new_hand = Hand()
        new_hand.game = start_game
        new_hand.user = player
        rand_card = random.choice(Card.objects.all())
        new_hand.card = rand_card
        new_hand.save()
    start_game.stage = STAGES[index_of_stage+1][0]
    start_game.save()
    return redirect('rooms/' + update_game.room)




    
    
        


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
