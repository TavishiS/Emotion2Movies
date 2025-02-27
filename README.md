This is a repo to build a creative project for our Software Engineering course.

# Emotion (in speech) based movie player
We will recommend movie on the basis of your emotions :)

# Content of repo :
1. Folder "UML files" containing UML diagrams
2. Folder "Project" containing Project files
3. Folder "instance" containing local database (sql-lite)
4. Folder "learning" containing things that are created just for understanding new tools and technology

# To run app :
1. clone repository
2. Install requirements.txt
3. open repository directory 
4. run 'app.py' (relative path to nevigate : "\Project\app.py")
5. check your api key for using "recommandation using prompt" on https://openrouter.ai/settings/keys


# How we run this : 
1. created AWS EC2 instance.
2. created dir "project" and cloned this repo in that dir
3. created vertual python environment in ./Emotion2Movies/Project via "python3 -m venv SE_env"
4. activate SE_env via "source SE_env/bin/activate"
5. installed requirements.txt via "pip install -r requirements.txt"
6. install gunicorn via "pip install gunicorn" (works for Ubuntu/linux etc)
7. run command "gunicorn -b 0.0.0.0:5000 app:app" to start app
9. now gunicorn will start website at our EC2's local server which is available for us at public address of our EC2
10. link for website : [http://public_ip_of_aws_instance:5000/](http://13.60.73.59:5000/) 
note : website will be live when we start from our side  :)
11. to check which processes are running on your ubuntu machine; run command "top -U \<specific user\>"
12. to stop gunicorn; run command "sudo killall gunicorn"
