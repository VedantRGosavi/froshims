#implements a registration form, storing the registrants in a dict, with error messages
from flask import Flask, redirect, render_template, g, request
import sqlite3

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('froshims.db')
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
SPORTS = ["BasketBall", "Soccer", "Cricket", "American Football"]


@app.route('/')
def index():
    return render_template("index.html", sports=SPORTS)

@app.route('/deregister', methods=['POST'])
def deregister():
    
    #forget the registrant 
    db = get_db().cursor()
    id = request.form.get("id")
    if id: 
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    get_db().commit()
    return redirect("/registrants")

@app.route("/register", methods=["POST"])
def register():
    
    #Validate Submission 
    db = get_db().cursor()
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")
    
    #Remember registrant
    db.execute("INSERT INTO registrants (name, sport) VALUES (?, ?)", (name, sport))
    get_db().commit()
    
    #Confirm registration
    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    db = get_db().cursor()
    db.execute("SELECT * FROM registrants")
    registrants = [dict(id=row[0], name=row[1], sport=row[2]) for row in db.fetchall()]
    return render_template("registrants.html", registrants=registrants)


    