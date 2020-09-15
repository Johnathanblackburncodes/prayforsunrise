from django.db import models

# Create your models here.


class Card(models.Model):
    pass
    #ImageURL - Should this be it's own seperate class?
    #CharacterName
    name = models.CharField(max_length=20)
    #Description/Special Text
    description = models.TextField(max_length=250)

class Game(models.Model):
    pass
    #Host - many-to-one / many(games) can have the same one (host)
    host = models.FOREIGNKEY(User, on_delete=models.CASCADE)

    #Room


    #Round
    round = models.IntegerField()

class Profile(models.Model):
    pass
    #AvatarURL - move to seperate class 
    image = models.ForeignKey(User, on_delete=models.CASCADE)

    #Bio
    bio = bio.CharField(max_length=200)

    #Eaten - boolean?**********
    #eaten = models.

    #Executed - boolean?*******


    #Won/End Game Status - boolean?********



class User(models.Model):
    pass
    username = models.CharField(max_length=20)
    image = models.ForeignKey(Avatar, on_delete=models.CASCADE)



#should images be seperate for the user?

#User avatar
class Avatar(models.Model):
    pass
    #URL
     url = models.CharField(max_length=200)

     #user associated
     user = models.ForeignKey(User, on_delete=models.CASCADE)

# image for the card
class Image(models.Model):
    pass 
    #URL
    url = models.CharField(max_length=200)

    #card associated
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

