from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Import game logic from UI.py concepts
class GameState:
    def __init__(self):
        self.player_position = 0
        self.tile_types = self.define_tile_types()
        self.player_money = 1500  # Starting money
        
    def define_tile_types(self):
        """Define tile types matching your UI.py logic"""
        types = ['START'] + ['RANDOM'] * 39
        
        special_positions = {
            0: 'START',
            10: 'EXCHANGE',
            20: 'JACKPOT',
            30: 'TRAP',
            5: 'NEWS',
            15: 'NEWS',
            25: 'NEWS',
            35: 'NEWS',
        }
        
        for pos, tile_type in special_positions.items():
            types[pos] = tile_type
        
        random_types = ['BONUS', 'LUCKY', 'CHANCE', 'NEWS', 'QUEST']
        for i in range(40):
            if types[i] == 'RANDOM':
                types[i] = random.choice(random_types)
        
        return types

game = GameState()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roll')
def roll_dice():
    dice = random.randint(1, 6)
    game.player_position = (game.player_position + dice) % 40
    tile_type = game.tile_types[game.player_position]
    
    # Add event logic based on tile type
    event_message = handle_tile_event(tile_type)
    
    return jsonify({
        "dice": dice,
        "position": game.player_position,
        "tile": tile_type,
        "event": event_message,
        "money": game.player_money
    })

def handle_tile_event(tile_type):
    """Handle events when landing on different tiles"""
    if tile_type == 'BONUS':
        game.player_money += 100
        return "You received $100 bonus!"
    elif tile_type == 'TRAP':
        game.player_money -= 50
        return "You fell into a trap! Lost $50"
    elif tile_type == 'JACKPOT':
        game.player_money += 500
        return "JACKPOT! You won $500!"
    # Add more tile event handlers
    return f"You landed on {tile_type}"