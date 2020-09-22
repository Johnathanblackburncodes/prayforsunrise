# Putting some game logic here
from .models import Profile, Game, Card, Hand, STAGES, STATUS, ROLES
G_STAGES = [t[0] for t in STAGES if t[0]]
G_ROLES = [r[0] for r in STAGES if r[0]]

def game_next_stage(game):
    players = game.user.all()

    for stage in G_STAGES[(G_STAGES.index(game.stage)+1):-1]
        #check if there are any players in the next stage, if so return that stage
        for player in players
            #check if the player's role matches the next stage
            if ROLES[G_ROLES.index(player.hand.role)][1] = STAGES[G_STAGES.index(stage)][1]
            return stage
    #now return our next useful Stage

def game_clear_hands(game):
    try:
        success = objects.filter(game=game).delete()
    except:
        return(False)
    return(success)