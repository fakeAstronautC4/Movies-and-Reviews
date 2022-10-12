"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    new_user = User(email=email, password=password)
    return(new_user)
    
def create_movie(title, overview, release_date, poster_path):
    new_movie = Movie(
        title=title, 
        overview=overview, 
        release_date=release_date, 
        poster_path=poster_path,
    )
    return(new_movie)

def get_all_movies():
    return Movie.query.all()

def get_users():
    return User.query.all()    

def create_rating(score, movie, user):
    new_rating = Rating(score=score, movie=movie, user=user)
    return(new_rating)
    
# def get_user_by_email(email):
#     verified = User.query.filter_by(email = email).first()
#     return(verified)














########################################################################


if __name__ == '__main__':
    from server import app
    connect_to_db(app)