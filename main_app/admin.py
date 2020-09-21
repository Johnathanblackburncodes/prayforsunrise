from django.contrib import admin
from .models import Profile, Game, Card, Hand, Photo
# Register your models here.

admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Game)
admin.site.register(Card)
admin.site.register(Hand)

