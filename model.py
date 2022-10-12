"""Models for movie ratings app."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Replace this with your code!


def connect_to_db(flask_app, db_uri="postgresql://alons:hqO1451**Ken@localhost:5432/ratings", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


#################################### CLASSES ##########################################
class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(30), nullable = False)

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = password


    # ratings = a list of Rating objects

    def __repr__(self):
      return f'<User user_id={self.user_id} email={self.email}>'


class Movie(db.Model):

    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key =True, autoincrement = True)
    title = db.Column(db.String, unique = True, nullable = False)
    overview = db.Column(db.Text, nullable = False)
    release_date = db.Column(db.DateTime, nullable = False)
    poster_path = db.Column(db.String, nullable = False, unique = True)

    # def __init__(self, title, overview, release_date, poster_path):
    #     self.title = title
    #     self.overview = overview
    #     self.release_date = release_date
    #     self.poster_path = poster_path

    # ratings = a list of Rating objects

    def __repr__(self):
        return (f"Movie: {self.title}\nSynopsis: {self.overview}\nRelease Date: {self.release_date}")


class Rating(db.Model):
    __tablename__ = 'ratings'

    # def __init__(self, score, movie_id, user_id):
    #     self.score = score
    #     self.movie_id = movie_id
    #     self.user_id = user_id

    rating_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    movie = db.relationship('Movie', backref = 'ratings')
    user = db.relationship('User', backref = 'ratings')
    # variable = db.relationship(argument1, argument2)
    # argument1 ---> Name of the class the attribute will be associated with
    # argument2 ---> Name of the attribute that will be used to reference the related instance(s) of this class
    # backref   ---> Means the relationship goes both ways
    # >>> user = User.query.get(1)  # Get a user by primary key

    # >>> user.ratings  # Wow!!
    # [<Rating rating_id=1 score=2>, <Rating rating_id=2 score=4>]
    def __repr__(self):
        return (f"Rating ID: {self.rating_id}\nScore: {self.score}")

##############################################################################

if __name__ == "__main__":
    from server import app
    connect_to_db(app)


