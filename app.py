from flask import Flask, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
import mysql.connector

mydb = mysql.connector.connect(
  host="sql6.freesqldatabase.com",
  user="sql6507600",
  password="bNLE7Re8hC",
  database="sql6507600"
)

mycursor = mydb.cursor()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        email = request.form.get("email")
        name = request.form.get("name")
        crypto = request.form.get("crypto")
        sql = "SELECT * FROM users WHERE name=%s AND email=%s"
        vals = (name, email, )
        mycursor.execute(sql, vals)

        myresult = mycursor.fetchall()
        if(len(myresult) != 0):
            return render_template("register.html", mycontent = "Name and email is already registered!")
        else:
            sql = "INSERT INTO users (email, name, crypto) VALUES (%s, %s, %s)"
            vals = (email, name, crypto, )
            mycursor.execute(sql, vals)
            return render_template("register.html", mycontent = "Registration was successful. Enjoy your emails!")
