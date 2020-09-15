# Pray For Sunrise

Pray for Sunrise is an online interactive gaming lobby where users can join a "game room", play Pray for Sunrise with others, and communicate via chat. 


## Developers 

- [Nathan Childress](https://github.com/NathanChildress)
- [Johnathan Blackburn](https://github.com/Johnathanblackburncodes)
- [Sweet Van Loan](https://github.com/sweetvanloan) 

## Related Links

[Pitchdeck](https://docs.google.com/presentation/d/1vTCrukX5KumksbjCIKZLBv_ovEB0LWxSSjetG7AxC7A/edit?usp=sharing)

[Trello Board](https://trello.com/b/zA6ZqdWY/werewolf)

## Technologies and Tools 

- Python
- Django
- Heroku
- PostreSQL


## User Stories 

- AAU, I want to see a landing page.
- AAU, I want to be prompted to login if I am not logged in. 
- AAU, I want to be able to sign up if I do not already have an account.
- AAU, I want to be able to start a new game.
- AAU, I want to be able to complete one game and be prompted to start another game.
- AAU, I want to be assigned a character in a game.
- AAU, I want to be able to see my character information.
- AAU, I want to be able to chat with other players as I am playing the game.
- AAU, I want to be able to only see my character screen whilst other players perform their "nighttime" activities.
- AAU, I want to be able to vote on which player to execute.
- AAU, I want to be able to see a timer, so that I know how much time the other players and I have to decide on who to execute and convince other players who to execute
- AAU, I want to see a screen telling me who won and who lost.
- AAU, I want to only be able to access a game when I am logged in.


## Game Logic 

- Each User is given a card, describing their role. While three cards stay in the center.
- All players "go to sleep", and thus are unaware of any night activities by players with special abilities.
- At night, players with special abilities will perform their abilities in a certain order, unbeknownst to other players.
- Once night is over, players will have a limited amount of time to discuss who may or may not be the werewolf and convince one another to vote for or not vote for a player.
- When the timer is up, players will casts votes, whoever has the most votes is executed.
- If everyone voted for a different person, nobody dies.
- The "Villager" players win when at least one of the werewolves is executed OR if there are no werewolves and no one dies.
- The "Werewolf" players win when all the werewolves survive, and the "Tanner" player does not die.
- The "Tanner" player wins if said player dies.
- The "seer" player wakes during the night once. When the Seer wakes up, and they can either look at a player's card, or 2 cards in the center.
- the "drunk" player wakes during the night once. When the Drunk wakes up, they exchange their card with a card in the center. They DO NOT get to view their new card.
- The "troublemaker" wakes during the night once. When the Troublemaker player wakes up, they can switch 2 other player's cards, but does NOT view said cards. Additionally, said player cannot swap their own card
- The "troublemaker" wakes during the night once. When the Troublemaker player wakes up, they can switch 2 other player's cards, but does NOT view said cards. Additionally, said player cannot swap their own card

## ERD
![ERD Image](https://imgur.com/gfh09yi.jpg)

## Wireframes

![Lobby](https://imgur.com/eBepn7D.jpg)

![Action](https://imgur.com/pox61On.jpg)

![Landing](https://imgur.com/h9nMAr5.jpg)

## Screenshots



## Biggest Challenges

## Future Improvements