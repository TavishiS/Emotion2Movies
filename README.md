
# MoodFlix 
<p align="left">
  <img src="Project/static/MoodFlix_LOGO.png" alt="MoodFlix Logo" width="150">
</p>

## What We Do!
MoodFlix recommends movies based on your emotions. You can:
1. Fill out a form to search for movies based on your mood.
2. Provide a text prompt to find suitable movies.
3. Speak with our AI to get movie recommendations.
4. Enhance search results with a single click after viewing recommendations.

---

## How to Run the App
### Prerequisites
Before running the app, we recommend the following:
1. Our app is built using **Python 3.12.8**, so other Python versions may cause compatibility issues with required packages.
2. Create a **separate virtual environment** and activate it. This helps manage dependencies and avoid conflicts.
3. Download ffmpeg from https://ffmpeg.org/download.html and path of executable file in your environment variables to avoid any failure while using speech to text/ emotion.

### Steps to Run
1. Clone the repository:
   ```sh
   git clone https://github.com/TavishiS/Emotion2Movies.git
   ```
2. Enter the "Project" directory:
   ```sh
   cd Emotion2Movies/Project
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python app.py
   ```

---

## Website overlook 
<p align="center">
  <img src="UML%20files/working_image.png" alt="UML Diagram" width="600">
</p>

---

## Repository Structure
1. **UML files** - Contains UML diagrams.
2. **Project** - Main project files.
3. **Learning** - Experimental files for understanding new tools and technologies.
4. **MoM** - Minutes of Meetings, stored regularly.
5. **SRS** - Software Requirement Specification document.

---

## How We Deploy on AWS
1. Create an **AWS EC2 instance**.
2. Clone this repository in the home directory:
   ```sh
   git clone https://github.com/TavishiS/Emotion2Movies.git
   ```
3. Navigate to the "Project" directory:
   ```sh
   cd Emotion2Movies/Project
   ```
4. Create a virtual environment:
   ```sh
   python3 -m venv env
   ```
5. Activate the virtual environment:
   ```sh
   source env/bin/activate
   ```
6. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
7. Test by running:
   ```sh
   python app.py
   ```
   (Ensure all requirements are satisfied before proceeding.)
8. Start the app using Gunicorn:
   ```sh
   nohup gunicorn -b 0.0.0.0:5000 -w 4 -k gevent app:app >/dev/null 2>&1 &
   ```
   - `-w 4` sets the number of workers.
   - `-k gevent` optimizes request handling.
9. The website will be available at: [http://public_ip_of_aws_instance:5000/](http://65.0.176.225:5000/)
   *(Note: The website will only be live when we start it from our side.)*
10. To check running processes:
    ```sh
    top -U <specific_user>
    ```
11. To stop Gunicorn:
    ```sh
    pkill gunicorn
    ```

---

## Why Use Gunicorn with nohup?
- **nohup**: Keeps the process running even after logging out, useful for remote servers via SSH.
- **-b**: Binds the application to all allowed IPs.
- **-w**: Defines the number of workers for handling multiple requests.
- **-k gevent**: Sets worker type to "gevent", which efficiently handles hundreds of requests per worker.
- **>/dev/null 2>&1 &**: Suppresses logs and runs the process in the background.

---

<div class="container">
    <h1>Meet Our Contributors</h1>
    <p>Here are the amazing contributors who have helped build this project.</p>
    <div class="contributors" style="display: flex; flex-wrap: nowrap; overflow-x: auto; gap: 20px;">
        <div class="contributor" style="text-align: center; flex: 0 0 auto;">
            <img src="Project/static/contributors/dhruv.jpeg" alt="Dhruv Mishra" 
                 style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%;">
            <p><strong>Dhruv Mishra</strong></p>
            <p>b23cs1090@iitj.ac.in</p>
        </div>
        <div class="contributor" style="text-align: center; flex: 0 0 auto;">
            <img src="Project/static/contributors/shreekar.jpg" alt="Shreekar" 
                 style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%;">
            <p><strong>Shreekar</strong></p>
            <p>b23cs1069@iitj.ac.in</p>
        </div>
        <div class="contributor" style="text-align: center; flex: 0 0 auto;">
            <img src="Project/static/contributors/tavishi.jpg" alt="Tavishi Srivastava" 
                 style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%;">
            <p><strong>Tavishi Srivastava</strong></p>
            <p>b23cs1101@iitj.ac.in</p>
        </div>
        <div class="contributor" style="text-align: center; flex: 0 0 auto;">
            <img src="Project/static/contributors/ripu.jpeg" alt="Ripu Daman Singh" 
                 style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%;">
            <p><strong>Ripu Daman Singh</strong></p>
            <p>b23cs1057@iitj.ac.in</p>
        </div>
        <div class="contributor" style="text-align: center; flex: 0 0 auto;">
            <img src="Project/static/contributors/ekta.jpeg" alt="Ekta Saini" 
                 style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%;">
            <p><strong>Ekta Saini</strong></p>
            <p>b23cs1018@iitj.ac.in</p>
        </div>
        <div class="contributor" style="text-align: center; flex: 0 0 auto;">
            <img src="Project/static/contributors/sanyam.jpeg" alt="Sanyam Kabra" 
                 style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%;">
            <p><strong>Sanyam Kabra</strong></p>
            <p>b23cs1063@iitj.ac.in</p>
        </div>
    </div>
</div>


Enjoy using MoodFlix! 🎬😊

