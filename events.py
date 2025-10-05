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
        # Group project collaboration – +happiness

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

        case 7:
            print("You feel like you have too many assignments and are under a huge pressure.")
            player.mood += 10

        case 8:
            print('Your friend is pleading with you: "Today is my girlfriend’s birthday, so I can’t go to my part-time job. Please help me cover my shift!"')
            choice = yn_input("You’re already exhausted. Will you help him? (Y/N): ")

            if choice:
                player.mood -= 20
                player.balance += 30
                print("You reluctantly agree. Your friend almost bursts into tears and insists you take his pay as thanks.")
            else:
                print('Your friend sighs: "Never mind, I’ll figure something out myself."')

        case 9: 
            x = random.randint(20, 50)
            print(f"You’re feeling unwell and spend £{x} on medicine.")
            player.balance -= x
            player.mood -= round(x / 2.5)

        case 10:
            x = random.randint(30, 80)
            print(f"Your laptop slipped off the desk! You spend £{x} to get it repaired.")
            player.balance -= x
            player.mood -= round(x / 2.5)

#happy events
        case 11:
            lottery_win = random.randint(20, 100)
            print(f"You win £{lottery_win} in a campus lottery!")
            player.balance += lottery_win
            player.mood += round(lottery_win / 2) 

        case 12:
            extra_pay = random.randint(5, 50)
            print(f"Due to your hard work during shifts, you have been awarded a bonus pay £{extra_pay}.")
            player.balance += extra_pay
            player.mood += round(extra_pay/2)

        case 13: 
            textbook = random.randint(3, 10)
            print(f"Someone bought the second hand textbook that you posted up, you've sold £{textbook}.")
            player.balance += textbook 
            player.mood += round(textbook/2)

        case 14:
            prize = random.randint(10, 50)
            print(f"You have entered a hackathon and are nominated as the winner, you receive £{prize} as the prize, well done!")
            player.balance += prize
            player.mood += round(prize/2.5)

#sad events
        case 15:
            car = random.randint(50, 150)
            print (f"During your ride to school you realised that there is a breakage in your car, £{car} is needed for fixing. ")
            player.balance -= car
            player.mood -= round(car/10)

        case 16:
            scam = random.randint(50, 100)
            print (f"You fall into a scam when trying to buy concert tickets online, £{scam} was lost unfortunately. ")
            player.balance -= scam
            player.mood -= round(scam/8)

        case 17:
            repair_cost = random.randint(3, 8)
            print("You spill coffee on your study notes. You buy a new coffee + reprint notes.")
            player.balance -= repair_cost
            player.mood -= round(repair_cost / 1.5)

#choice events
        case 18:
            ticket_cost = 15
            choice = yn_input(f"Your friend invited you to your favourite band’s concert, the ticket costs £{ticket_cost}. Are you willing to join? (Y/N): ")
            if choice:
                if player.balance >= ticket_cost:
                    player.balance -= ticket_cost
                    print("You go to the concert and had an amazing time! ")
                    player.balance -= ticket_cost
                    player.mood += 20
                else:
                    print("You realise that you dont have enough money for the ticket.")
                    player.mood -= 10
            else:
                print("You skip the concert to study. Stay productive, but you feel left out. ")
                player.mood -= 5

        case 19:
            hours = random.randint(5, 15)
            wage = 10
            choice = yn_input("Your boss asks if you can do extra shifts over the weekend, however that means you need to miss your best friend’s birthday party. Would you choose to do an extra shift? (Y/N): ")
            if choice:
                earnings = hours * wage
                print(f"You work {hours} hours and earn £{earnings}. ")
                player.balance += earnings
                player.mood -= round(hours / 2) 
            else:
                print("You decline the shift and decided to go to the party, You had fun but realised that you are getting a bit broke for spending.")
                player.balance -= (hours / 2) 
                player.mood += 10

        case 20:
            gift_price = 10
            choice = yn_input("It’s your best friend’s birthday soon! Would you like to buy her a gift? (Y/N): ")
            if choice:
                if player.balance >= gift_price:
                    player.balance -= gift_price
                    print("You went to the party and had an amazing time with your friends!")
                    player.balance -= gift_price
                    player.mood += 15
                else:
                    print("You realise that you dont have enough money for any gifts.")
                    player.mood -= 10
            else:
                print("You didn't go to the party, your friend is unhappy because of it.")
                player.mood -= 15

        case 21:
            trip = 50
            choice = yn_input("You got invited for a weekend trip, are you willing to join? (Y/N): ")
            if choice:
                if player.balance >= trip:
                    player.balance -= trip
                    print("You went to the trip and had an amazing time with your friends!")
                    player.balance -= trip
                    player.mood += 15
                else:
                    print("The trip is out of your budget, you can't make it in the end.")
                    player.mood -= 10
            else:
                print("You didnt go to the trip, however you manage to get a lit of work done over the weekends.")
                player.mood -= 10

        case 22:
            # Check player has money
            if player.balance <= 0:
                print("Unfortunately, you don’t have any money to save right now.")
                exit

            print("You decide it’s time to start saving some money for the future.")
            print("How would you like to save?")
            print("Option A: Short-term fixed deposit (3 months, higher interest, but you can’t withdraw early).")
            print("Option B: Long-term fixed deposit (1 year, best interest, but money is locked for a long time).")
            print("Option C: Flexible savings account (lower interest, but you can withdraw anytime).")
            print("Option D: Do not save.")

            # Ask user how much to save
            while True:
                try:
                    amount = float(input(f"How much would you like to save? (Enter 0 to cancel, Available: £{player.balance:.2f}): "))
                    if amount == 0:
                        print("You decided to keep your money as cash—safe but not very profitable.")
                        break  # Exit the amount input and skip saving
                    elif 0 < amount <= player.balance:
                        break
                    else:
                        print("Please enter a valid amount within your balance.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            # Ask for saving option
            while True:
                choice = input("Please enter A/B/C/D: ").upper().strip()
                if choice in ['A', 'B', 'C', 'D']:
                    break
                else:
                    print("Invalid choice. Please enter A, B, C, or D.")

            # Apply effects
            if choice == 'A':
                player.add_investment("short", amount)
                print("You can’t use this money for 3 months, but it’ll earn 10% interest at maturity.")

            elif choice == 'B':
                player.add_investment("long", amount)
                print("It will grow steadily over a year (30% interest), but you can’t touch it meanwhile.")

            elif choice == 'C':
                player.add_investment("flexible", amount)
                print("It earns low interest daily but you can withdraw anytime.")

            else:  # D
                print("You decided to keep your money as cash—safe but not very profitable.")
