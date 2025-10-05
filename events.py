import random

def yn_input(prompt):
    while True:
        choice = input(prompt)
        if choice.lower() == "y":
            return True
        if choice.lower() == "n":
            return False

def event(player, event_id):
    match event_id:
        case 1:
            x = random.randint(10,50)
            print(f"You find £{x} on the street. Lucky you!")
            player.balance += x
            player.mood += round(x/2.5)

        case 2:
            x = random.randint(10,50)
            print(f"You are robbed by some plucky seagulls. You lose £{x}.")
            player.balance -= x
            player.mood -= round(x/2.5)

        case 3:
            x = random.randint(1,5)
            choice = yn_input("Marnix asks you to invest £50 in TrumpCoin. Do you accept? (Y/N): ")
            if choice:
                if x == 1:
                    print("You somehow turn a tidy profit of £50. Don't let it get to your head!")
                    player.balance += 50
                    player.mood += 25
                elif x == 2:
                    print("You manage to break even before losing any money. Close shave!")
                else:
                    print("You lose everything. Maybe invest in something better next time?")
                    player.balance -= 50
                    player.mood -= 30


