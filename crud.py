
from flask.templating import _default_template_ctx_processor
from flask_sqlalchemy import _record_queries
from model import db, User, Comment, Restroom, connect_to_db



def create_user(email, password, username):
    user = User(email=email, password=password, username=username)
    db.session.add(user)
    db.session.commit()
    
    return user


def get_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)
    


def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def create_restroom(name, address, city):
    restroom = Restroom(restaurant_name=name, address=address,city=city)
    db.session.add(restroom)
    db.session.commit()

    return restroom

def get_restroom_by_address(address):
    return Restroom.query.filter(Restroom.address == address).first()

def get_all_restrooms_by_city(city):
    return Restroom.query.filter(Restroom.city == city).all()

def get_restroom_by_id(restroom_id):
    return Restroom.query.get(restroom_id)



def create_comment(text, user, restroom):
    comment = Comment(comment_text=text, user=user,restroom=restroom)