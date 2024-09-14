from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time/')
def time_page():
    return render_template('time.html')

@app.route('/api/time/')
def api_time():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(current_time=current_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
