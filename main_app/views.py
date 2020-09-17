from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from django.contrib.auth.models import User
from .forms import GameForm
from .models import Game, Hand

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
