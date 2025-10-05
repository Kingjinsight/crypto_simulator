# General_objects
import random

class Player:
    def __init__(self, player_id, name, color=(255, 0, 0)):
        self.id = player_id
        self.name = name
        self.position = 0
        self.cash = 10000
        self.portfolio = {}  # add with {crypto name, number}
        self.color = color  # player color
        self.laps_completed = 0  # how many circule the player finished

    def add_cash(self, amount):
        self.cash += amount

    def remove_cash(self, amount):
        self.cash -= amount
        if self.cash < 0:
            self.cash = 0

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

class Event:
    def __init__(self, name, event_type, change_percent):
        self.name = name
        self.describe = None
        self.event_type = event_type
        self.change_percent = change_percent

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

