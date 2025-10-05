import random

def event(player, event_id):
    match event_id:
        case 1:
            x = random.randint(10,50)
            player.balance += x
            player.mood += round(x/2.5)
            return f"You find £{x} on the street. Lucky you!"

        case 2:
            x = random.randint(10,50)
            player.balance -= x
            player.mood -= round(x/2.5)
            return f"You are robbed by some seagulls. You lose £{x}."