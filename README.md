This is a repo to build a creative project for our Software Engineering course.

# Emotion (in speech) based movie player
We will recommend movie on the basis of your emotions :)

# Content of repo :
1. Folder "UML files" containing UML diagrams
2. Folder "Project" containing Project files
3. Folder "instance" containing local database (sql-lite)
4. Folder "learning" containing things that are created just for understanding new tools and technology

# Requirements :
Activate your env.
1. 'pip install flask' (for Web application)
2. 'pip install -U Flask-SQLAlchemy' (for local database (if you want to use that))
3. 'pip install ray' (for parallel computation with CPU)

# To run app :
1. clone repository
2. Install requirements.txt
3. open repository directory 
4. run 'app.py' (relative path to nevigate : "\Project\app.py")

# How we run this : 
1. created AWS EC2 instance.
2. created dir and cloned this repo
3. created vertual python environment
4. installed requirements.txt via "pip install -r requirements.txt"
5. install gunicorn
6. run command "gunicorn -b 0.0.0.0:5000 app:app"
7. now gunicorn will start website at our EC2's local server which is available for us at public address of our EC2
8. link for website : [http://public_ip_of_aws_instance:5000/](http://13.60.224.246:5000) 
note : website will be live when we start from our side  :)
