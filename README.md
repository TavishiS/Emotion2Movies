This is a repo to build a creative project for our Software Engineering course.

# Emotion (in speech) based movie player
We will recommend movie on the basis of your emotions :)

# Content of repo :
1. Folder "UML files" containing UML diagrams
2. Folder "Project" containing Project files
3. Folder "instance" containing local database (sql-lite)
4. Folder "learning" containing things that are created just for understanding new tools and technology
5. Folder "MoM" to store Minutes of the Meetings on a regular basis
6. Folder "SRS" to store requirements document : https://1drv.ms/w/c/8039175bd1074318/EbC3cY1hmiVAhf5rpwh-T7IBVD-M7zzY2zVgdHsKSOSQVg?e=aoOIDt

# To run app :
1. clone repository
3. Install requirements.txt
4. open repository directory
5. open "Project" directory (important!)
6. run 'app.py'


# How we run this : 
1. create AWS EC2 instance.
2. clone this repo in home
3. create vertual python environment in ./Emotion2Movies/Project via "python3 -m venv env"
4. activate env via "source env/bin/activate"
5. installed requirements.txt via "pip install -r requirements.txt"
6. run app.py via "python app.py" and terminate that (for confirming all requirements are satisfied or not.)
7. run command "nohup gunicorn -b 0.0.0.0:5000 -w 4 -k gevent app:app >/dev/null 2>&1 &" to start app (using -w for set number of workers, -k for set type of worker (gevent is very good for handeling multiple requests like hundreds of requests per worker))
9. now gunicorn will start website at our EC2's local server which is available for us at public address of our EC2
10. link for website : [http://public_ip_of_aws_instance:5000/](http://65.0.176.225:5000/) 
note : website will be live when we start from our side  :)
11. to check which processes are running on your ubuntu machine; run command "top -U \<specific user\>"
12. to stop gunicorn; run command "pkill gunicorn"

# Why while gunicorn :
***nohup*** Keeps the process running even after logout so Useful when running on a remote server via SSH.

***-b*** : to bind all allowed ip's

***-w*** : to set number of workers

***-k gevent*** : to set type of workers to "gevent" that can handle hundreds of requests per worker

***>/dev/null 2>&1 &*** :	Suppresses all logs & runs in background
