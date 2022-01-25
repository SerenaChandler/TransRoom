"""Server for restroom app."""

from flask import (Flask, render_template, request, flash, jsonify, session, url_for, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
import requests
from authlib.integrations.flask_client import OAuth
import bcrypt
import werkzeug
import os
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


oauth = OAuth(app)
google = oauth.register(
name="google",
client_id="535415915919-hbmr4bug2qfob84lp7dqt56n9u0o7fpe.apps.googleusercontent.com",
client_secret=os.environ["CLIENT_SECRET"],
access_token_url='https://accounts.google.com/o/oauth2/token',
access_token_params=None,
authorize_url='https://accounts.google.com/o/oauth2/auth',
authorize_params=None,
api_base_url='https://www.googleapis.com/oauth2/v1/',
client_kwargs={'scope': 'openid profile email'}
)


@app.route("/")
def homepage():
    restrooms = ""
    user = None
    if session.get("user_id"):
        user = crud.get_user_by_id(session["user_id"])
    # return render_template("index.html", user=user)
    return render_template("homepage.html", restrooms=restrooms, searched_restrooms=restrooms)


@app.route("/bowlmates")
def pal_page():
    matches = None
    if session.get("user_id"):
        return render_template('pals.html', matches=matches)
    else:
        flash("Must be logged in to use Bowlmates")

    return redirect('/')

@app.route('/find-pals')
def find_pals():

    if session.get("user_id"):
        user = crud.get_user_by_id(session["user_id"])
    # print("\n", "*"*20, user.comments,"\n")
    restrooms = []
    for comment in user.comments:
        if comment.restroom_id not in restrooms:
            restrooms.append(comment.restroom_id)
    # print("\n", "*"*20, restrooms,"\n")

    users = crud.get_users()
    matched_users = []
    for user in users:
        if user.user_id != session["user_id"]:
            for comment in user.comments:
                if comment.restroom_id in restrooms and user.to_dict() not in matched_users:
                    matched_users.append(user.to_dict())
    # print("\n", "*"*20, matched_users,"\n")

    return jsonify(matched_users)
    return render_template('/pals.html', matches=matched_users)


@app.route('/add-friend', methods=["POST"])
def add_friend():
    friend_id = request.json.get('id')
    print("\n", "*"*20, friend_id,"\n")
    friend = crud.get_user_by_id(friend_id)
    print("\n", "*"*20, friend,"\n")
    user = crud.get_user_by_id(session["user_id"])
    if friend in user.following:
        print('already friends')
        return jsonify({'success': True, "status": "Already Friends!" })
    else:
        print('added friend')
        crud.add_friend(user, friend)

        print("\n", "*"*20, user.following,"\n")
        print("\n", "*"*20, friend.followers,"\n")
        return jsonify({'success': True, "status": "Added friend!" })
    

   
    
@app.route('/delete-friend/<user_id>')
def delete_friend(user_id):
    user = crud.get_user_by_id(session["user_id"])
    friend = crud.get_user_by_id(user_id)
    crud.delete_friend(user, friend)
    return redirect("/user")


@app.route("/login")
def login_page():
    if session.get("user_id"):
        flash("You're already logged in")
    else:
        sess = session.get("user_id")   
        return render_template("login.html", sess=sess)
    return redirect("/")


@app.route('/google-login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    print("\n", "*"*20, token,"\n")
    resp = google.get('userinfo')
    resp.raise_for_status()
    profile = resp.json()
    print("\n", "*"*20, profile,"\n")
    # do something with the token and profile
    if crud.get_user_by_email(profile['email']):
        user = crud.get_user_by_email(profile['email'])
        session["user_id"] = user.user_id
    else:
        hashed_password = bcrypt.hashpw(profile['id'].encode('utf8'), bcrypt.gensalt())
        username = profile['given_name']
        crud.create_user(profile['email'], hashed_password, username)
        user = crud.get_user_by_email(profile['email'])
        session["user_id"] = user.user_id
    return redirect('/')



@app.route("/logout")
def logout():
    if session.get("user_id"):
        session.clear()
        flash("successfully logged out.")
    else:
        flash("Already logged out")
    return redirect("/")




@app.route("/create-user", methods=["POST"])
def create_user():
    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")
    user = crud.get_user_by_email(email)
    existing_username = crud.get_user_by_username(username)

    if not email:
        flash("Please enter email")
    elif not password:
        flash("Please enter password")
    elif not username:
        flash("Please enter username")
    elif user:
        flash("That email is already associated with an account.")
    elif existing_username:
        flash("That username is already associated with an account.")
    else:
        hashed_password = werkzeug.security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        crud.create_user(email, hashed_password, username)
        flash("Account created!")
    
    return redirect("/login")





@app.route("/handle-login", methods=["POST"])
def handle_login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
  

    if user:
        if werkzeug.security.check_password_hash(user.password, password):
            if user:
                if user.email == email:
                    session["user_id"] = user.user_id
                    flash("Logged in!")
                    return redirect("/")
            else:
                flash("Incorrect password or email. Please try again")
    else:
        flash("Incorrect password or email. Please try again")

    return redirect("/login")




@app.route("/user")
def to_user_profile():
    
    if session.get("user_id"):
        user = crud.get_user_by_id(session["user_id"])
        print("\n", "*"*20, user.following,"\n")
        return render_template("user.html", user=user)
    else:
        flash("Login to see your user page")
        return redirect("/")

@app.route("/add")
def to_add_page():
    return render_template("add-restroom.html")



@app.route("/add-restroom", methods=["POST"])
def add_restroom():

    street = request.form.get("address").strip()
    name = request.form.get("name").strip()
    city = request.form.get("city").strip()
    ADA = request.form.get("ada")

    if crud.get_restroom_by_address(street):
        flash("This restroom is already in the database")
    elif not street or not name or not city:
        flash("Must enter address/city/name of business") 

    else:
        if ADA:
            ADA=True
            crud.create_restroom(name, street, city, ADA)
            flash("Added restroom!")
        else:
            ADA=False
            crud.create_restroom(name, street, city, ADA)
            flash("Added restroom!")


 
    return redirect("/add")



@app.route("/handle-search")
def search_handler():
    APIURL = "http://www.refugerestrooms.org/api/v1/restrooms/search?page=1&per_page=30&offset=0&query="
    search = request.args.get("search").lower()
    ADA = request.args.get("ada")
    
    query = APIURL + search
    restrooms = ""
    user = None
    if session.get("user_id"):
        user = crud.get_user_by_id(session["user_id"])

    if crud.get_restroom_by_city(search):
        if ADA == "True":
            searched_restrooms = crud.get_all_accessible_restrooms_by_city(search)
        else:
            searched_restrooms = crud.get_all_restrooms_by_city(search)
        restroom_scores=[]
        for searched_restroom in searched_restrooms:
            total_score=0
            averaged_score=0
            i=0.00000000000000000001
            for comment in searched_restroom.comments:
                if comment.rating:
                    total_score += int(comment.rating)
                    i+=1
            averaged_score = total_score/i
            final_rating = ("{:.1f}".format(averaged_score))
            restroom_scores.append(final_rating)
            

    else:
        res = requests.get(query)
        restrooms = res.json()  

        for restroom in restrooms:
            current_restroom = crud.get_restroom_by_address(restroom["street"])
            if not current_restroom:
                crud.create_restroom(restroom['name'],restroom['street'],restroom['city'],restroom['accessible'])

        if ADA == "True":
            searched_restrooms = crud.get_all_accessible_restrooms_by_city(search)
        else:
            searched_restrooms = crud.get_all_restrooms_by_city(search)
        restroom_scores=[]
        for searched_restroom in searched_restrooms:
            total_score=0
            averaged_score=0
            i=0.00000000000000000001
            for comment in searched_restroom.comments:
                if comment.rating:
                    total_score += int(comment.rating)
                    i+=1
            averaged_score = total_score/i
            final_rating = ("{:.1f}".format(averaged_score))
            restroom_scores.append(final_rating)
    data = {}
    data['restrooms'] = searched_restrooms
    data['scores'] = restroom_scores
    data['user'] = user
    print("\n", "*"*20, data,"\n")
    # return json.dumps(searched_restrooms)
    return render_template("homepage.html", searched_restrooms=searched_restrooms,user=user, restroom_scores=restroom_scores)





@app.route("/restroom/<restroom_id>")
def see_comments(restroom_id):
    restroom = crud.get_restroom_by_id(restroom_id)
    comments = {}
    rating = {}
    comments_and_ratings = {}
    for i, comment in enumerate(restroom.comments):
        comments[i] = comment.comment_text
    for i, comment in enumerate(restroom.comments):
        rating[i] = comment.rating
    comments_and_ratings['comments'] = comments
    comments_and_ratings['rating'] = rating
    return comments_and_ratings
    




@app.route("/comment/<restroom_id>", methods = ["POST"])
def add_comment(restroom_id):
    # print("\n", "*"*20, restroom_id,"\n")
    text = request.json.get("text")
    rating = request.json.get("rating")
    restroom = crud.get_restroom_by_id(restroom_id)
    print("\n", "*"*40, restroom,"\n")
    if session.get("user_id"):
        user = crud.get_user_by_id(session["user_id"])
        crud.create_comment(text=text,user=user,restroom=restroom, rating=rating)
        total_score=0
        averaged_score=0
        i=0.00000000000000000001
        for comment in restroom.comments:
            if comment.rating:
                    total_score += int(comment.rating)
                    i+=1
            averaged_score = total_score/i
            new_rating = ("{:.1f}".format(averaged_score))

        return jsonify({'success': True, "status": "thank you for your comment", "rating": new_rating, "restroom_id": restroom_id })
    else:
        return jsonify({'success': False, "status": "must be logged in to leave comment"})



@app.route("/delete/comment/<comment_id>")
def delete_comment(comment_id):
    crud.delete_comment(comment_id)
    return redirect("/user")


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app, echo=False)
    app.run(host="0.0.0.0", debug=True)