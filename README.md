# 🐦‍⬛ Bird Watching Forum


## 🌟 Highlights

- Create a profile to log in
- Post your sightings on a dynamic forum
- Edit, view or delete your posts as needed
- Interact with posts through likes and comments


## ℹ️ Overview

Hello, my name is Katie. I am a student at Colorado Technical University studying software engineering. I created this project to showcase my skills with Flask, Python, SQL, Jinja, and HTML. My files are organized in an MVC format with flask_app, config, controllers, models, and templates folders. This bird watcing forum consists of 4 different SQL tables that all interact with each other. The goal of this software is to display my expertise in connecting and modifying databases with SQL and Python and displaying the data dynamically with Jinja and HTML.


### ✍️ Authors

Katie Chickering - https://github.com/katiechickering


## 🚀 Usage

```bash
python server.py
 * Serving Flask app 'flask_app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
 * Running on http://localhost:5001
```
Run 'python server.py' in your terminal. Then, copy and paste http://localhost:5001 into your browser to view the application!


## ⬇️ Installation

```bash
pip install -r requirements.txt
```
First, install all the required packages with the code above. Then, run bird_watching.sql in your MySQL local database software to save the database. Finally, change the user and password in lines 8 and 9 of flask_app/config/mysqlconnection.py to match your database credentials. Please see below for a reference.

```py
connection = pymysql.connect(host = 'localhost',
                            user = 'root', # Line 8
                            password = 'rootroot', # Line 9
                            db = db,
                            charset = 'utf8mb4',
                            cursorclass = pymysql.cursors.DictCursor,
                            autocommit = False)
```

## 💭 Feedback and Contributing

If you found this insightful or if you have suggestions, please start a [discussion](https://github.com/katiechickering/bird-watching/discussions/1)!