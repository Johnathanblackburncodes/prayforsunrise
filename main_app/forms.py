from django.forms import ModelForm
from .models import Game

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['room']

class SetupGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['room']