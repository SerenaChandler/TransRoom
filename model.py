"""models for restroom search app"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


friend = db.Table(
    'friends',
    db.Column('friends_id', db.Integer, primary_key=True),
    db.Column('f1_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('f2_id', db.Integer, db.ForeignKey('users.user_id'))
)


class User(db.Model):
    """a user"""

    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    following = db.relationship(
        'User',
        secondary=friend,
        primaryjoin=user_id == friend.c.f1_id,
        secondaryjoin=user_id == friend.c.f2_id,
        backref='followers'
    )

    def to_dict(self):
        user = {}
        user['id'] = self.user_id
        user['email'] = self.email
        user['username'] = self.username
        user['password'] = self.password
        return user

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Comment(db.Model):
    """a comment left by a user"""

    __tablename__='comments'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    restroom_id = db.Column(db.Integer, db.ForeignKey("restrooms.restroom_id"))
    comment_text = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Integer)

    user = db.relationship("User", backref="comments")
    restroom = db.relationship("Restroom", backref="comments")

    def to_dict(self):
        comment = {}
        comment['id'] = self.comment_id
        comment['user'] = self.user_id
        comment['restroom'] = self.restroom_id
        comment['text'] = self.comment_text
        comment['rating'] = self.rating
        return comment

    def __repr__(self):
        return f"<Comment comment_id={self.comment_id} comment_text={self.comment_text} rating={self.rating}>"

class Restroom(db.Model):
    """a restroom"""

    __tablename__='restrooms'
    restroom_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String(), nullable=False)
    ADA = db.Column(db.Boolean, nullable=False, default=False)


    def to_dict(self):
        restroom = {}
        restroom['id'] = self.restroom_id
        restroom['name'] = self.restaurant_name
        restroom['address'] = self.address
        restroom['city'] = self.city
        restroom['ADA'] = self.ADA
        return restroom

    def __repr__(self):
        return f"""<Restroom restroom_id={self.restroom_id} 
        address={self.address} restaurant_name={self.restaurant_name} ADA={self.ADA}>"""


class Message(db.Model):

    __tablename__='messages'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_text = db.Column(db.String(), nullable=False)
    recipient = db.Column(db.String(), nullable=False)
    sender = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"""<Message message_id={self.message_id} 
        sender_name={self.sender} recipient_name={self.recipient}>"""

def connect_to_db(flask_app, db_uri="postgresql:///comments", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)