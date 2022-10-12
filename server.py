

import email
from wsgiref.util import request_uri
from flask import (Flask, render_template, request, flash, session, redirect, url_for)
import os

from sqlalchemy import null
from model import connect_to_db, db, Movie, User, Rating
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'extremely_secret'
# a random key used to encrypt your cookies and save send them to the browser
app.jinja_env.undefined = StrictUndefined

########################### ROUTES ###########################

@app.route("/")
def homepage():
    return render_template ("homepage.html")





@app.route("/movies")
def all_movies():
    all_movies = crud.get_all_movies()
    return render_template ("movies.html", all_movies = all_movies)

@app.route("/movies/<movie_id>")
def movie_details(movie_id):
    detailed_mov = Movie.query.get(int(movie_id))
    return render_template ("movie_details.html", detailed_mov = detailed_mov) 

@app.route("/users")
def users():
    all_users = crud.get_users()
    return render_template("users.html", all_users=all_users)

@app.route("/users", methods=["POST"])
def register():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")
    tobechecked = crud.get_user_by_email(user_email)
    if tobechecked == None:
        new_user = crud.create_user(user_email, user_pass)
        db.session.add(new_user)
        db.session.commit()
        flash("User Created")
    else:
        flash("There is an user already using that email")
    return redirect("/")

@app.route("/login", methods=["POST", 'GET'])
def login():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")
    user_q = User.query.filter_by(email = user_email).first()
    if user_q.email == user_email and user_q.password == user_pass:
        session['user_id'] = user_q.user_id
        flash("Logged in successfully!")
        
    else:
        flash("User not found... REGISTER")
    return redirect("/")

@app.route('/logout')
def logout():
    if 'user_in' in session:
        del session['user_id']
        flash('You have successfully logged out')
    else:
        flash("You are not logged in")
    return redirect('/')

@app.route("/users/<user_id>")
def user_details(user_id):
    detailed_user = User.query.get(user_id)
    return render_template ("user_details.html", detailed_user=detailed_user)

@app.route("/review", methods=['POST'])
def review():
    if 'user_id' not in session:
        flash("You have to log in to review movies")
        
    else:
        review_score = int(request.form.get("score"))
        movie_id = int(request.form.get("mov_id"))
        user_id = int(session["user_id"])
        print(review_score, movie_id, user_id)
        new_rating = Rating(score=review_score, movie_id=movie_id, user_id=user_id)
        db.session.add(new_rating)
        db.session.commit()
        flash("Thanks for sharing!")
    return redirect("/movies")

################################################################
if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)