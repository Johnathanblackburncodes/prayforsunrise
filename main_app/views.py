from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_eventstream import send_event

import uuid, random
import boto3 


from .forms import GameForm, SetupGameForm
from .models import Profile, Game, Card, Hand, STAGES, Photo


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'prayforsunrise'


V_STAGES = [t[0] for t in STAGES if t[0]]



def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def rules(request):
    return render(request, 'rules.html')

def room(request, room_name):
    try:
        game = Game.objects.get(room=room_name)
        room_user = User.objects.get(pk=request.user.id)
        game.user.add(room_user)
    except:
        print(game)
        return redirect('/')
    hands = Hand.objects.filter(game=game)
    return render(request, 'game/room.html', {
        'room_name': room_name,
        'game': game,
        'hands': hands
    })


def profile(request, user_id):
    profile = Profile.objects.get(puser=user_id)
    image = ''
    
    try:
        image = Photo.objects.get(profile=profile.id)
        print('image is,', image)

    except:
        print('No Photo Found')

    print('this is PROFILE', profile)
    print('this is user_id', user_id)
    return render(request, 'profile.html', {
        'profile': profile,
        'image': image
    })

### GAME FUNCTIONS

def add_game(request):
  form = GameForm(request.POST)
  new_room = ''
  if form.is_valid():
    new_game = form.save(commit=False)
    try:
        new_game.room = uuid.uuid4().hex[:4]
        new_game.host_id = request.user.id
        new_game.stage = STAGES[0][0]
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
    start_game = Game.objects.get(room=update_game.room)
    index_of_stage = V_STAGES.index(start_game.stage)
    players = start_game.user.all()
    
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

    print(f'send an SSE to {update_game.room}')
    send_event(update_game.room, 'board-updated', {'text': 'board_updated'})
    return redirect('rooms/' + update_game.room)

def push_next_stage(request, room_name):
    game = Game.objects.get(room=update_game.room)
    index_of_stage = V_STAGES.index(start_game.stage)
    game.stage = STAGES[index_of_stage+1][0]

def generate_board(request, room_name):
    game = Game.objects.get(room=room_name)
    print(f'This is our Game{game}, this is our room_name{room_name}')
    hands = Hand.objects.filter(game=game)
    return HttpResponse(render_to_string("game/fragments/board.html", {"room_name":room_name, "hands":hands, "game":game, "request":request}))


### OTHER PAGES    

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(puser=user)
            profile.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def add_photo(request, user_id, profile_id):
    photo_file = request.FILES.get('photo-file', None)
    print('user ID on 141 = ', user_id)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(id=profile_id)
            photo = Photo(image=url, puser=user, profile=profile)
            photo.save()
            print('user ID AFTER SAVE =', user_id)
        except Exception as e:
            print('e =', e)
            print('Oops, something went wrong. Please try again.')
    return redirect('profile', user_id) 


