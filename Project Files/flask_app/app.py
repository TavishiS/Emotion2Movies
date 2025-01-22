from flask import Flask     
app = Flask(__name__)   # Flask constructor 
  
# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')       
def hello(): 
    return 'Hello , write your name in the URL after the /'  

@app.route('/<name>')
def hello_world(name):     
    return 'Well done %s' % name 
  
if __name__=='__main__':
    app.run(debug=True)