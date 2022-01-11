"""models for restroom search app"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

class User(db.Model):
    """a user"""

    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username} email={self.email}>"


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

    def __repr__(self):
        return f"<Comment comment_id={self.comment_id} comment_text={self.comment_text} rating={self.rating}>"

class Restroom(db.Model):
    """a restroom"""

    __tablename__='restrooms'
    restroom_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Restroom restroom_id={self.restroom_id} address={self.address} restaurant_name={self.restaurant_name}>"




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