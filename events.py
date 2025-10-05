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

        case 4:
            print("Your friend invites you to join a student club for one month (£25 membership fee).")

            choice = yn_input("Do you want to join? (Y/N): ")

            if choice:
                x = random.randint(1, 3)
                if x == 1:
                    print("You have a great time and meet new friends! Worth every penny.")
                    player.balance -= 25
                    player.mood += 20
                elif x == 2:
                    print("It was fun but also time-consuming. You enjoy it a bit but lose some sleep.")
                    player.balance -= 25
                    player.mood += 10
                else:
                    print("You didn’t really click with anyone, but at least you tried something new.")
                    player.balance -= 25
            else:
                print("You decided not to join. You saved money, but maybe missed out on some fun.")
                player.mood -= 5

        # Part-time job – +money, -happiness
        # Studying in the library – +happiness
        # Scholarship received – +money
        # Group project collaboration – +happiness
        # Exam preparation – -happiness

        case 5:
            print("You need to buy textbooks - and they are not cheap.")
            print("Option A: Rent books - £30")
            print("Option B: Buy used books - £50") 
            print("Option C: Buy new books - £80")
            
            while True:
                choice = input("Please enter A/B/C: ").upper().strip()
                if choice == 'A':
                    player.balance -= 30
                    print("You rented the textbooks. -£30")
                    break
                elif choice == 'B':
                    player.balance -= 50
                    print("You bought used textbooks. -£50")
                    break
                elif choice == 'C':
                    player.balance -= 80
                    print("You bought new textbooks. -£80")
                    break
                else:
                    print("Invalid choice. Please enter A, B, or C.")

        case 6:
            print("You went to the library today. You feel more fulfilled and happier.")
            player.mood += 20

            
