from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def firstPage():
    return render_template('about.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/form_input')
def form_input():
    return render_template('form_input.html')

@app.route('/prompt_input')
def prompt_input():
    return render_template('prompt_input.html')

@app.route('/recommendations')
def recommandetions():
    return render_template('recommendations.html')

if __name__ == '__main__':
    app.run(debug=True)