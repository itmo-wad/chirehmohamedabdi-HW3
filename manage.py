import os
from turtle import title
from flask import Flask, redirect, render_template, send_file, send_from_directory, url_for, request, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime




app = Flask(__name__)
#This is my secret key
app.config['SECRET_KEY'] = b'X\x98\xb6\xaf5;\x00\xcb\xcf\xba\xbc\xb4\x98/\xc1`'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Hw2'
mongo = PyMongo(app)
#Redirect default route to the profile page route
@app.route("/")
def Index():
    #Display Sign In page 
    posts = mongo.db.posts.find()
    return render_template("profile.html", titles=posts)

@app.route("/SignIn", methods=['GET','POST'])
def SignIn():
    if request.method == "GET":
        return render_template("form_auth.html")
    else:
         #store username and password from form
        username = request.form.get('username')
        password = request.form.get('password')

        #check username
        username_val = mongo.db.users.find_one({'username':username})
        password_val = mongo.db.users.find_one({'password':password})
        if  username_val and password_val:
            session["username"] = username
            return redirect(url_for('.secret_page', username=username))
        #if a username doesn't existed
        else:
            flash('password or username incorrect ')
            return render_template("form_auth.html")

@app.route("/signUp", methods=['GET','POST'])
def SignUp():
    if request.method == "GET":
        return render_template("Sign_up.html")
    else:
         #store username and password from form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        username_val = mongo.db.users.find_one({'username':username})
        if username_val :
            flash('Username exists !!!')
            return render_template("Sign_up.html")
        else :
            user_input = {'username': username, 'email': email, 'password': password}
            mongo.db.users.insert_one(user_input)
            flash('Success !')
            return render_template("Sign_up.html")
        #check username
        

@app.route('/profile?<string:username>')
def secret_page(username):
    posts = mongo.db.posts.find()
   
    return render_template("profile.html", username=username, titles=posts)

@app.route('/new_Posts', methods=['GET','POST'])
def new_posts():
    if request.method == "GET":
        return render_template("new_posts.html")
    else :
         #store Title and Message from form
        title = request.form.get('title')
        message = request.form.get('message')
        user_connected = session["username"]
        now = datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")

        MessageInsert = {'title': title, 'Message': message, 'user': user_connected, 'time': time}
        mongo.db.posts.insert_one(MessageInsert)
        flash('Post submit !!!')
        return redirect(url_for('.secret_page', username=user_connected))

@app.route('/profile')
def profile():
    return render_template("profile.html")

#Define the icon of the site
@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static","favicon.ico","assets/icon/icon2.png")
#Customize the error page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found_page.html'), 404
if __name__ == "__main__":
    app.run("localhost",port=5000,debug=True)