from django.db import models

# Create your models here.


class Card(models.Model):
    #ImageURL - Made into a seperate class
    avatar = models.FOREIGNKEY(Avatar, on_delete=models.CASCADE)


    #CharacterName
    name = models.CharField(max_length=20)

    #Description/Special Text
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name

class Game(models.Model):
    #Host - many-to-one / many(games) can have the same one (host)

    host = models.FOREIGNKEY(User, on_delete=models.CASCADE)
    host = models.FOREIGNKEY(User, on_delete=models.CASCADE)
    card = models.FOREIGNKEY(Card, on_delete=models.CASCADE)

    #Room - should rooms be their own class or a list - and how many?
    room = models.models.IntegerField()


    #Round - functionality needed to make rounds count += / however there is only one round in ONUW? Or are we wanting more rounds?/functional
    # round = models.IntegerField()

class Profile(models.Model):
    #AvatarURL - move to seperate class 
    image = models.ForeignKey(User, on_delete=models.CASCADE)

    #Bio
    bio = bio.CharField(max_length=200)

    #Eaten - boolean?**********// per nathan - changed to int/user 
    #eaten = models.
    eaten = models.models.IntegerField()

    #Executed - boolean?*******// per nathan - changed to int/user 
    executed = models.models.IntegerField()


    #Won/End Game Status - boolean?********// per nathan - changed to int/user 
    status = models.models.IntegerField()



class User(models.Model):
    username = models.CharField(max_length=20)
    image = models.ForeignKey(Avatar, on_delete=models.CASCADE)

    def __str__(self):
        return self.username



#should images be seperate for the user?/below

#User avatar
class Avatar(models.Model):
    #URL
     url = models.CharField(max_length=200)

     #user associated
     user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
    return f"Photo for card_id: {self.user} @{self.url}"

# image for the card
class Image(models.Model): 
    #URL
    url = models.CharField(max_length=200)

    #card associated
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
     return f"Photo for card_id: {self.card} @{self.url}"

