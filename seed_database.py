import os
import json
from random import randint, choice
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    ################## MOVIES ###################
    movie_data = json.loads(f.read())
    movie_in_db = []
    for movies in movie_data:
        title, overview, poster_path = (movies['title'], movies['overview'], movies['poster_path'])
        release_date = datetime.strptime(movies['release_date'], "%Y-%m-%d")
        
        new_movie = crud.create_movie(title, overview, release_date, poster_path)
        movie_in_db.append(new_movie)
    
    model.db.session.add_all(movie_in_db)
    # model.db.session.commit()

    ################## USERS ###################
    
for i in range(10):
    email = f"random@email{i}.com"
    password = "randomize!!"

    new_user = crud.create_user(email, password)
    model.db.session.add(new_user)

    ################# RATINGS ##################
    for _ in range(10):
    #   ^  not interested in the iterator value therefore replaced by a '_'
        score = randint(1 , 5)
        movie = choice(movie_in_db)

        new_rating = crud.create_rating(score, movie, new_user)
        model.db.session.add(new_rating)

model.db.session.commit()