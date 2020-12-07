import os

from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = os.environ.get("MySQL_DB_PASS")
app.config["MYSQL_DB"] = "usercredentials"

mysql = MySQL(app)


@app.route("/home", methods=["GET"])
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/registerorlogin", methods=["GET", "POST"])
def registerOrLogin():
    if request.method == "GET":
        return render_template("login_and_register.html")
    elif (
        request.method == "POST"
        and "rname" in request.form
        and "rpassword" in request.form
    ):
        name = request.form["rname"]
        password = request.form["rpassword"]
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(name, password) VALUES(%s, %s)", (name, password)
        )
        mysql.connection.commit()
        return render_template("succesful_registration.html")
    elif (
        request.method == "POST"
        and "name" in request.form
        and "password" in request.form
    ):
        name = request.form["name"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM users WHERE name = % s AND password = % s",
            (
                name,
                password,
            ),
        )
        account = cur.fetchone()

        if account:
            session["loggedin"] = True
            session["name"] = account[0]
            msg = "Logged in successfully !"
            return render_template("index.html", msg=msg)
    else:
        msg = "Please fill out the form !"
    return render_template("invalid_credentials.html")


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.secret_key = "124o1b54b4i12@#$%#$^#"
    app.run(host="0.0.0.0",port=5000)