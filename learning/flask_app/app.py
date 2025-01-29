from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
   sno = db.Column(db.Integer, primary_key=True)
   movie1 = db.Column(db.String(200), nullable=False)
   movie2 = db.Column(db.String(200), nullable=False)
   option = db.Column(db.String(100), nullable=False)
   date_created = db.Column(db.DateTime, default=datetime.utcnow)

   def __repr__(self) -> str:
         return f"{self.sno} - {self.title}"
      
      
@app.route('/', methods=['GET', 'POST'])
def home():
   allPosts = Todo.query.all()
   return render_template('home.html', allPosts=allPosts)

@app.route('/deleterow/<int:sno>', methods=['GET', 'POST'])
def delete(sno):
   post = Todo.query.filter_by(sno=sno).first()
   db.session.delete(post)
   db.session.commit()
   return redirect('/')

@app.route('/update_data', methods=['GET', 'POST'])
def update():
   return redirect('/')

@app.route('/movie', methods=['GET', 'POST'])
def movie():
   movie1_name = None
   movie2_name = None
   if request.method == 'POST':
      movie1_name = request.form['movie1']
      movie2_name = request.form['movie2']
      option_name = request.form['option']
   if movie1_name and movie2_name:
      obj=Todo(movie1=movie1_name, movie2=movie2_name, option=option_name)
      db.session.add(obj)
      db.session.commit()
      return render_template('movie.html', movie_name=movie1_name)
   else:
      return redirect('/')


if __name__ == '__main__':
   app.run(debug=True)