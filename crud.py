
from flask.templating import _default_template_ctx_processor
from flask_sqlalchemy import _record_queries
from model import db, User, Comment, Restroom, Message, connect_to_db



def create_user(email, password, username):
    user = User(email=email, password=password, username=username)
    db.session.add(user)
    db.session.commit()
    
    return user


def get_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_username(username):
    return User.query.filter(User.username == username).first()
    

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def add_friend(user, friend):
    user.following.append(friend)
    db.session.commit()

def delete_friend(user, friend):
  for i, following in enumerate(user.following):
      if following.user_id == friend.user_id:
          user.following.pop(i)
          db.session.commit() 

def create_restroom(name, address, city, ada):
    restroom = Restroom(restaurant_name=name, address=address,city=city.lower(), ADA=ada)
    db.session.add(restroom)
    db.session.commit()

    return restroom

def get_restroom_by_address(address):
    return Restroom.query.filter(Restroom.address == address).first()

def get_all_restrooms_by_city(city):
    return Restroom.query.filter(Restroom.city.like(city)).all()


def get_all_accessible_restrooms_by_city(city):
    return Restroom.query.filter(Restroom.city.like(city), Restroom.ADA == True).all()


def get_restroom_by_city(city):
    return Restroom.query.filter(Restroom.city.like(city)).first()

def get_restroom_by_id(restroom_id):
    return Restroom.query.get(restroom_id)



def create_comment(text, user, restroom, rating):
    comment = Comment(comment_text=text, user=user,restroom=restroom, rating=rating)
    db.session.add(comment)
    db.session.commit()
    return comment


def delete_comment(comment_id):
    deleted_comment = Comment.query.filter(Comment.comment_id == comment_id).first()
    db.session.delete(deleted_comment)
    db.session.commit()
     

def create_friend(name,user):
    friend = Friend(friend_name=name,user=user)
    db.session.add(friend)
    db.session.commit()
    return friend


def create_message(message_text, sender, recipient):
    message = Message(message_text=message_text, sender=sender.username, recipient=recipient.username)
    db.session.add(message)
    db.session.commit()
    return message

def get_messages_by_user_and_recipient(user, recipient):
    print(recipient)
    # return Message.query.filter(Message.sender == user.username, Message.recipient == recipient.username).all()
    return Message.query.filter(((Message.sender == user.username) & (Message.recipient == recipient.username)) | ((Message.sender == recipient.username) & (Message.recipient == user.username))).all()