from flask import Flask, request
import subprocess

app = Flask(__name__)
process = None  # Store the script process

@app.route('/start', methods=['POST'])
def start_script():
    global process
    if process is None or process.poll() is not None:
        process = subprocess.Popen(['python', '/home/nao/scripts/record-and-respond.py'])
        return 'Script started', 200
    else:
        return 'Script already running', 400

@app.route('/stop', methods=['POST'])
def stop_script():
    global process
    if process is not None and process.poll() is None:
        process.terminate()
        return 'Script stopped', 200
    else:
        return 'No script running', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

