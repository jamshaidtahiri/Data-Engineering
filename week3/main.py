from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/hello')    
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)