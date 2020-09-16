from django.db import models
from django.contrib.auth.models import User
# Create your models here.
​

class Card(models.Model):
    # ImageURL - Made into a seperate class/changed to inclass
    # avatar = models.FOREIGNKEY(Avatar, on_delete=models.CASCADE)
    imgurl = models.CharField(max_length=200)
​
​
    #CharacterName
    name = models.CharField(max_length=20)
​
    #Description/Special Text
    description = models.TextField(max_length=250)
​
    def __str__(self):
        return self.name
​
class Game(models.Model):
    #Host - many-to-one / many(games) can have the same one (host)
​
    host = models.ForeignKey(User, on_delete=models.CASCADE)
​
    #Each game will have many cards
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
​
    #Room - should rooms be their own class or a list - and how many?
    #-Nathan Change to string to denote the game\room our sockets open
    room = models.CharField(max_length=20)
​
    #We will need a many to many field for Users in a game connection I think.
​
​
    #stage - functionality needed to make stages count += / however there is only one round in ONUW? Or are we wanting more rounds?/functional
    #round looks like a keyword going to change to 'stage'
    stage = models.IntegerField()
​
class Profile(models.Model):
    #AvatarURL - move to seperate class 
    #Charfield change to url string
    image = models.CharField(max_length=200)
​
    #Bio
    bio = models.CharField(max_length=20)
​
    #Eaten - boolean?**********// per nathan - changed to int/user 
    #eaten = models.
    eaten = models.IntegerField()
​
    #Executed - boolean?*******// per nathan - changed to int/user 
    executed = models.IntegerField()
​
​
    #Won/End Game Status - boolean?********// per nathan - changed to int/user 
    #we might change this to an ENUM of some kind but integer will give us flexibility while we work it out.
    status = models.IntegerField()
​
    #link our profile to a user
    puser = models.ForeignKey(User, on_delete=models.CASCADE)
​
​
​
​
​
#should images be seperate for the user?/below
​
#User avatar
# class Avatar(models.Model):
#     #URL
#      url = models.CharField(max_length=200)
​
#      #user associated
#      user = models.ForeignKey(User, on_delete=models.CASCADE)
​
#     def __str__(self):
#         return f"Photo for card_id: {self.user} @{self.url}"
​
​
​
# # image for the card
# class Image(models.Model):
#     #URL
#     url = models.CharField(max_length=200)
​
#     #card associated
#     card = models.ForeignKey(Card, on_delete=models.CASCADE)
​
#     def __str__(self):
#         return f"Photo for card_id: {self.card} @{self.url}"
