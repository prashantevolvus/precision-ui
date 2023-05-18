from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute')
def execute_script():
    process = subprocess.Popen(['script/pre-exec.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in iter(process.stdout.readline, ''):
        socketio.emit('message', line.rstrip())
    return "Script execution initiated"

@socketio.on('connect')
def handle_connect():
    emit('message', 'Connected to server')

if __name__ == '__main__':
    socketio.run(app, debug=True)
