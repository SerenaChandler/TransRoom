"""Server for restroom app."""

from flask import (Flask, render_template, request, flash, jsonify, session, redirect)
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
    return render_template("homepage.html", restrooms=restrooms, searched_restrooms=restrooms)






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
        flash("successfully logged out.")
    return redirect("/")





@app.route("/create-user", methods=["POST"])
def create_user():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user:
        flash("That email is already associated with an account.")
    else:
        crud.create_user(email, password)
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
        flash("Incorrect password or email. Please try again")
    return redirect("/login")




@app.route("/user")
def to_user_profile():
    
    if session.get("user_id"):
        user = crud.get_user_by_id(session["user_id"])
        return render_template("user.html", user=user)
    else:
        flash("Login to see your user page")
        return redirect("/")

@app.route("/add")
def to_add_page():
    return render_template("add-restroom.html")



@app.route("/add-restroom", methods=["POST"])
def add_restroom():

    street = request.form.get("address")
    name = request.form.get("name")
    city = request.form.get("city")
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
    print("\n", "*"*20, ADA,"\n")
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
                crud.create_restroom(restroom['name'],restroom['street'],restroom['city'].lower(),restroom['accessible'])

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

    return render_template("homepage.html", restrooms=restrooms, searched_restrooms=searched_restrooms,user=user, restroom_scores=restroom_scores)





@app.route("/restroom/<restroom_id>")
def see_comments(restroom_id):
    restroom = crud.get_restroom_by_id(restroom_id)
    return render_template("restroom-comments.html", restroom=restroom)




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