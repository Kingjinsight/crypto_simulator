from flask import Flask, render_template
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play_game():
    # Run your pygame file in a separate process
    python_exec = sys.executable
    subprocess.Popen([python_exec, os.path.join(os.getcwd(), "UI.py")])
    return "Game started! You can close this tab."

if __name__ == '__main__':
    app.run(debug=True)
