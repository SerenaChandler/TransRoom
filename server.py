"""Server for restroom app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
import requests

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def homepage():
    restrooms = ""
    return render_template("homepage.html", restrooms=restrooms)


@app.route("/login")
def login_page():
    if session.get("user_id"):
        flash("You're already logged in")
    else:
        sess = session.get("user_id")   
        return render_template("login.html", sess=sess)
    return redirect("/")

@app.route("/logout")
def logout():
    if session.get("user_id"):
        session.clear()
    return redirect("/")

@app.route("/create-user", methods=["POST"])
def create_user():
    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")
    user = crud.get_user_by_email(email)
    if user:
        flash("That email is already associated with an account.")
    else:
        crud.create_user(email, password, username)
        flash("Account created!")
    
    return redirect("/login")


@app.route("/handle-login", methods=["POST"])
def handle_login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user:
        if user.email == email and user.password == password:
            session["user_id"] = user.user_id
            flash("Logged in!")
            return redirect("/")
    else:
        flash("Invalid login credentials.")
    return redirect("/login")


@app.route("/handle-search")
def search_handler():
    APIURL = "http://www.refugerestrooms.org/api/v1/restrooms/search?page=1&per_page=10&offset=0&query="
    search = request.args.get("search")
    query = APIURL + search
    print(query)
    res = requests.get(query)
    restrooms = res.json()
    print(restrooms)



    return render_template("homepage.html", restrooms=restrooms)



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)