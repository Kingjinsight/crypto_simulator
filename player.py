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
        if self.mood > 100:
            self.mood = 100
        if self.mood < 0:
            self.mood = 0
        print(f"You have £{self.balance} and are feeling {self.mood_to_word(self.mood)}.\nIt is day {self.space+1} of month {self.month}.")

    def next_day(self):
        self.space += 1
        if self.space > 27:
            self.space %= 28
            self.month += 1
        