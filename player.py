class Player:
    def __init__(self):
        self.space = 0
        self.balance = 0
        self.mood = 70
        self.month = 1

    @staticmethod
    def mood_to_word(mood):
        if mood <= 20:
            return "terrible"
        elif 20 < mood <= 40:
            return "bad"
        elif 40 < mood <= 60:
            return "average"
        elif 60 < mood <= 80:
            return "good"
        elif 80 < mood <= 100:
            return "amazing"

    def status(self):
        if self.mood < 0:
            self.mood_punishment()
            if self.game_over:
                return  # The game is over
            
        if self.mood > 100:
            self.mood = 100

        print(f"You have £{self.balance} and are feeling {self.mood_to_word(self.mood)}.\nIt is day {self.space+1} of month {self.month}.")

    def next_day(self):
        self.space += 1
        if self.space > 27:
            self.space %= 28
            self.month += 1
        
    # user may spend money to travel to recover the mood to full to continue the game, or end the game if they give up or do not have enough money
    def mood_punishment(self):
        """Punishment mechanism for handling low mood"""
        print("\n⚠️  Warning: Your mood has dropped to a critical level!")
        print("You're experiencing severe emotional distress...")
        
        if self.balance < 200:
            print("💔 You don't have enough money for a recovery trip.")
            print("The emotional burden becomes too much to bear...")
            print("You leave the university due to emotional problems.")
            self.game_over = True
        else:
            print("You have two options:")
            print("A: Spend £200 on a wellness trip to recover completely")
            print("B: Continue as is (risking academic performance)")
            
            while True:
                choice = input("Choose A or B: ").upper().strip()
                if choice == 'A':
                    self.balance -= 200
                    self.mood = 100
                    print("✈️  You went on a relaxing trip.")
                    print("By the time you returned, your mood had completely recovered!")
                    print(f"Remaining balance: £{self.balance}")
                    break
                elif choice == 'B':
                    print("You decide to push through without a break.")
                    print("The emotional burden becomes too much to bear...")
                    print("You leave the university due to emotional problems.")
                    self.game_over = True
                else:
                    print("Please enter A or B.")