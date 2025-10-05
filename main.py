# General_objects
import random

class Player:
    def __init__(self, player_id, name, color=(255, 0, 0)):
        self.id = player_id
        self.name = name
        self.position = 0
        self.cash = 10000
        self.portfolio = {}  # add with {crypto name, number}
        self.happness = 0
        self.color = color  # player color
        self.laps_completed = 0  # how many circule the player finished

    def change_cash(self, amount):
        self.cash += amount
        if self.cash < 0:
            self.cash = 0

    
    def change_happness(self, amount):
        self.happness += amount

    def buy_crypto(self, symbol, quantity, price): # symbol: name of the crypto
        cost = quantity * price
        if self.cash >= cost:
            self.cash -= cost
            if symbol in self.portfolio:
                self.portfolio[symbol] += quantity
            else:
                self.portfolio[symbol] = quantity
            return True
        return False

    def sell_crypto(self, symbol, quantity, price):
        if symbol in self.portfolio and self.portfolio[symbol] >= quantity:
            self.portfolio[symbol] -= quantity
            self.cash += quantity * price
            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]
            return True
        return False

    def get_total_assets(self, market):
        total = self.cash
        for symbol, quantity in self.portfolio.items():
            if symbol in market.prices:
                total += quantity * market.prices[symbol]
        return total


class CryptoMarket:
    def __init__(self):
        self.prices = {
            'BTC': 120000.0,
            'ETH': 4500.0,
            'DOGE': 0.25
        }
        self.history = []  # prices of all cryptos in history
        self.save_history()

    def save_history(self):
        self.history.append(self.prices.copy())
        if len(self.history) > 500:
            self.history.pop(0)

    def random_fluctuation(self):
        for symbol in self.prices:
            change = random.uniform(-0.05, 0.05)
            self.prices[symbol] *= (1 + change)
            if self.prices[symbol] < 0.01:
                self.prices[symbol] = 0.01
        self.save_history()

    def apply_news_event(self, symbol, change_percent):
        if symbol in self.prices:
            self.prices[symbol] *= (1 + change_percent / 100)
            if self.prices[symbol] < 0.01:
                self.prices[symbol] = 0.01
            self.save_history()

class Financial_Event:
    def __init__(self, name, event_type, change_percent):
        # change_percent is a dict, e.g. {"happiness": +10, "money": -20}
        self.name = name
        self.describe = None
        self.event_type = event_type
        self.change_percent = change_percent

    def apply(self, player):
        """Apply the event's effects to a Player instance."""
        print(f"Applying event: {self.name} to player: {player.name}")

        # Handle happiness change
        if "happiness" in self.change_percent:
            player.change_happness(self.change_percent["happiness"])
            print(f"  Happiness changed by {self.change_percent['happiness']} → {player.happness}")

        # Handle money change
        if "money" in self.change_percent:
            money_change = self.change_percent["money"]
            # Skip 'variable' events (like investment choices)
            if isinstance(money_change, (int, float)):
                player.change_cash(money_change * 100)  # e.g., +5 means +500 if you want scaling
                print(f"  Cash changed by {money_change * 100} → {player.cash}")
            else:
                print("  This event has a variable money effect (e.g. investment outcome).")


class Life_Event:
    def __init__(self, name, event_type, change_amount, change_happness_amount):
        self.name = name
        self.describe = None
        self.event_type = event_type
        self.change_amount = change_amount
        self.change_happness = change_happness_amount

    def apply(self, player):
        """Apply life event effects to the player."""
        print(f"Applying life event: {self.name} to player: {player.name}")
        player.change_cash(self.change_amount)
        player.change_happness(self.change_happness)
        print(f"  Cash: {player.cash}, Happiness: {player.happness}")

class GameData:
    def __init__(self):
        self.players = []
        self.crypto_market = CryptoMarket()
        self.current_turn = 0
        self.current_player_idx = 0

    def add_player(self, player):
        self.players.append(player)

    def get_current_player(self):
        if self.players:
            return self.players[self.current_player_idx]
        return None

    def next_turn(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        if self.current_player_idx == 0:
            self.current_turn += 1
            self.crypto_market.random_fluctuation()

def main():
    player = Player(player_id=1, name="Alice")

    # Learning & Income
    event1 = Financial_Event("Excellent Class Performance", "learning", {"happiness": +10, "money": +5})
    event2 = Financial_Event("Part-time Job", "learning", {"happiness": -5, "money": +20})
    event3 = Financial_Event("Exam Preparation", "learning", {"happiness": -10})
    event4 = Financial_Event("Scholarship Received", "learning", {"money": +30})

    # Living Expenses
    event5 = Financial_Event("Online Shopping", "expense", {"happiness": +8, "money": -10})
    event6 = Financial_Event("Cafeteria Top-up", "expense", {"money": -5})
    event7 = Financial_Event("Friend’s Birthday Gift", "expense", {"money": -15})

    # Finance & Investment
    event8 = Financial_Event("Finance Seminar", "investment", {"happiness": +5})
    event9 = Financial_Event("Regular Fund Investment", "investment", {"money": "variable"})
    event10 = Financial_Event("Yu’ebao Interest", "investment", {"money": +8})

    # Risk Events
    event11 = Financial_Event("Computer Repair", "risk", {"money": -25})
    event12 = Financial_Event("Unexpected Windfall", "risk", {"money": +50})
    event13 = Financial_Event("Skill Training", "risk", {"money": -10, "happiness": +10})

    # Store all events in a list for easy access or random selection
    events = [
        event1, event2, event3, event4, event5, event6, event7,
        event8, event9, event10, event11, event12, event13
    ]

    event3.apply(player)

    print(f"After event → Cash: {player.cash}, Happiness: {player.happness}")

if __name__ == "__main__":
    main()
