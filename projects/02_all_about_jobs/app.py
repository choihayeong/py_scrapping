from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<username>')
def contact(username):
    return f'Hello {username} how ya doin'

# app.run(host='0.0.0.0')