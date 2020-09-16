from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STAGES = (
    ('1', 'SETUP'),
    ('2', 'See Cards'),
    ('3', 'Villager'),
    ('4', 'Night Werewolf'),
    ('5', 'Night Seer'),
    ('6', 'Night Robber'),
    ('7', 'Troublemaker'),
    ('8', 'Night Drunk'),
    ('99', 'Complete')
)

ROLES = (
    ('V', 'Villager'),
    ('W', 'Werewolf'),
    ('T', 'Tanner'),
    ('S', 'Seer'),
    ('V', 'Villager'),
    ('R', 'Robber'),
    ('M', 'Troublemaker'),
    ('D', 'Drunk')
)

STATUS = (
    ('A', 'Alive'),
    ('E', 'Executed'),
    ('M', 'Murdered'),
    ('C', 'Consumed')
)

class Card(models.Model):
    #ImageURL - Made into a seperate class/changed to inclass
    # avatar = models.FOREIGNKEY(Avatar, on_delete=models.CASCADE)

    imgurl = models.CharField(max_length=200)


    #CharacterName
    name = models.CharField(max_length=20)

    #Description/Special Text
    description = models.TextField(max_length=250)

    role = models.CharField(
        # We're going to set the rounds to an ENUM for now
        # hard coding the night roles ATM but should probably
        # find a move flexible solution
        max_length=1,
        choices=ROLES,
        # We want to make sure we always default to Setup

        default=[0][0]
    )

    def __str__(self):
        return self.name

class Game(models.Model):
    #Host - many-to-one / many(games) can have the same one (host)

    host = models.ForeignKey(User, related_name="host", on_delete=models.CASCADE)

    #Each game will have many cards
    card = models.ManyToManyField(Card)

    #Room - should rooms be their own class or a list - and how many?
    #-Nathan Change to string to denote the game\room our sockets open
    room = models.CharField(max_length=100)

    #We will need a many to many field for Users in a game connection I think.
    user = models.ManyToManyField(User)

    #stage - functionality needed to make stages count += / however there is only one round in ONUW? Or are we wanting more rounds?/functional
    #round looks like a keyword going to change to 'stage'
    stage = models.CharField(
        # We're going to set the rounds to an ENUM for now
        # hard coding the night roles ATM but should probably
        # find a move flexible solution
        max_length=2,
        choices=STAGES,
        # We want to make sure we always default to Setup

        default=[0][0]
    )

class Hand(models.Model):
    #Every hand will need to belong to a Game and assign a player a card
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

class GameConditions(models.Model):
    #Every GC needs to be assigned to a Game
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(
        # We're going to set the player status to an ENUM 
        max_length=1,
        choices=STATUS,
        # We want to make sure we always default to Setup
        default=[0][0]
    )
    #make sure we have a card to reference roles
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class Profile(models.Model):
    #AvatarURL - move to seperate class 
    #Charfield change to url string
    image = models.CharField(max_length=200)

    #Bio
    bio = models.CharField(max_length=20)

    #Eaten - boolean?**********// per nathan - changed to int/user 
    #eaten = models.
    eaten = models.IntegerField()

    #Executed - boolean?*******// per nathan - changed to int/user 
    executed = models.IntegerField()


    #Won/End Game Status - boolean?********// per nathan - changed to int/user 
    #we might change this to an ENUM of some kind but integer will give us flexibility while we work it out.
    status = models.IntegerField()

    #link our profile to a user
    puser = models.ForeignKey(User, on_delete=models.CASCADE)







