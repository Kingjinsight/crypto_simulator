from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Simple Monopoly logic (no pygame)
player_position = 0
tile_types = ['START', 'BONUS', 'LUCKY', 'NEWS', 'TRAP'] * 8  # dummy example

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roll')
def roll_dice():
    global player_position
    dice = random.randint(1, 6)
    player_position = (player_position + dice) % 40
    return jsonify({
        "dice": dice,
        "position": player_position,
        "tile": tile_types[player_position]
    })

if __name__ == '__main__':
    app.run(debug=True)
