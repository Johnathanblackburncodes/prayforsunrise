from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
#parse out our templates for api calls 
from django.http import HttpResponse
from django.template.loader import render_to_string
#add our SSE command
from django_eventstream import send_event

import uuid, random
import boto3 #added for AWS pic SVL

#import our own forms and models
from .forms import GameForm, SetupGameForm
from .models import Profile, Game, Card, Hand, STAGES

#Needed for AWS SVL
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'prayforsunrise'

#need a list of keys from our stages tuple since we're only matching the first item, not the entire tuple
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
    hands = Hand.objects.filter(game=game)
    try:
        playerhand = Hand.objects.get(game=game, user=request.user)
    except:
        playerhand = {}
    print(f'playerhand is {playerhand}')
    return render(request, 'game/room.html', {
        'room_name': room_name,
        'game': game,
        'hands': hands,
        "playerhand": playerhand
    })

#added to create a place for photos and bios to live. 
def profile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    print('this is PROFILE', profile)
    return render(request, 'profile.html', {
        'profile': profile
    })

### GAME FUNCTIONS

def add_game(request):
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
        new_game.stage = STAGES[0][0]
        new_game.save()
        new_room = '/rooms/' + new_game.room
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
    #let the player's browsers update to the new cards
    print(f'send an SSE to {update_game.room}')
    send_event('gameroom', (update_game.room+'-updated'), {'text': 'board-updated'})
    #FIX: using a static room for SSE while we finish the game
    return redirect('rooms/' + update_game.room)

def push_next_stage(request, room_name):
    game = Game.objects.get(room=room_name)
    index_of_stage = V_STAGES.index(game.stage)
    #make sure we don't push past the last index
    if index_of_stage == V_STAGES[-1]:
        next_stage = STAGES[0][0]
    else:
        next_stage = STAGES[index_of_stage+1][0]
    game.stage = next_stage
    game.save()
    send_event('gameroom', (game.room+'-updated'), {'text': 'board-updated'})
    return HttpResponse("Next Stage")

def generate_board(request, room_name):
    game = Game.objects.get(room=room_name)
    print(f'This is our Game{game}, this is our room_name{room_name}')
    hands = Hand.objects.filter(game=game)
    try:
        playerhand = Hand.objects.get(game=game, user=request.user)
    except:
        playerhand = {}
    print(f'playerhand is {playerhand.card}')

    return render(request, "game/fragments/board.html", {
        "room_name":room_name,
        "hands":hands,
        "game":game,
        "playerhand":playerhand,
        "request":request
        })

def hand_reveal(request, hand_id):
    hand = Hand.objects.get(id=hand_id)
    print(f'{request.user} revealed {hand.user} is a {hand.card}')
    # Return the card revealed by the seer here. 
    response = f'<li class="card" ic-get-from="/hand/{hand_id}"> <img src={hand.card.imgurl}> </li>'
    return HttpResponse(response)

def hand_rob(request):
    print(request.user)
    try:
        card = request.POST.get('card','')
    except:
        pass
    print(card)
    try:
        victim_hand = Hand.objects.get(id=card)
        player_hand = Hand.objects.get(user=request.user)
    except: 
        print('Robber went wrong')
    swaplist = [victim_hand.card.id, player_hand.card.id]
    print(swaplist)
    try:
        new_victim_card = Card.objects.get(id=swaplist[1])
        new_player_card = Card.objects.get(id=swaplist[0])
    except:
        pass
    player_hand.card = new_player_card
    victim_hand.card = new_victim_card
    victim_hand.save()
    player_hand.save()

    print(victim_hand.card.id)
    print(f'{request.POST}')
    return render(request, "game/fragments/revealcard.html", {
        "hand":player_hand,
        "request":request
    })

def hand_troublemaker(request):
    card_list = request.POST.getlist('card')


### OTHER PAGES    

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
        return render('profile/<int:user_id>/', user_id=user_id )
