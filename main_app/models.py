from django.db import models
from django.contrib.auth.models import User


STAGES = (
    ('1', 'SETUP', ),
    ('2', 'See Cards'),
    ('3', 'Night'),
    ('4', 'Werewolf'),
    ('5', 'Seer'),
    ('6', 'Robber'),
    ('7', 'Troublemaker'),
    ('8', 'Drunk'),
    ('9', 'Day'),
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
        # find a more flexible solution
        max_length=2,
        choices=STAGES,
        # We want to make sure we always default to Setup

        default=[0][0]
    )

class Hand(models.Model):
    #Every hand will need to belong to a Game and assign a player a card
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    # Every Hand belongs to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    status = models.CharField(
        # We're going to set the player status to an ENUM 
        max_length=1,
        choices=STATUS,
        # We want to make sure we always default to Setup
        default=[0][0]
    )


class Profile(models.Model):
    bio = models.CharField(max_length=20)
    eaten = models.IntegerField(default=0)
    executed = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    puser = models.ForeignKey(User, on_delete=models.CASCADE)

class Photo(models.Model):
    image = models.CharField(max_length=200)
    puser = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

