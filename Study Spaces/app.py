from flask import Flask, render_template, request, url_for
import sqlite3
import datetime


app = Flask("__name__")

@app.route("/", methods=["GET"])
def home():
    conn = sqlite3.connect("studyspace.db")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Venue""")
    data = cur.fetchall()
    return render_template("home.html", data=data)

@app.route("/search/", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else: 
        conn = sqlite3.connect("studyspace.db")
        conn.close()

@app.route("/signin/", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        Venue, MatricNo, Name, Class = request.form["venue"], request.form["MatricNo"], request.form["Name"], request.form["Class"]
        
        x = datetime.datetime.now()
        time = x.strftime("%X")
        date = x.strftime("%x")
        timeout = "NULL"

        # create entry
        conn = sqlite3.connect('studyspace.db')
        conn.execute("""INSERT INTO 
                        Entry(MatricNo, VenueName, Date, TimeIn, TimeOut) VALUES (?,?,?,?,?)"""
                        , (MatricNo, Venue, date, time, timeout))
        conn.commit()
        conn.close()

        # Search if Student details already exist, if not, add
        conn = sqlite3.connect('studyspace.db')
        cur = conn.cursor()
        cur.execute("SELECT MatricNo FROM Student where MatricNo=?", (MatricNo,))
        data = cur.fetchall()
        if not data:
            conn = sqlite3.connect('studyspace.db')
            conn.execute("""INSERT INTO Student VALUES (?,?,?)""", (MatricNo, Name, Class))
            conn.commit()
            conn.close()
        else:
            pass  
        
        # Update venue capacity
        conn = sqlite3.connect('studyspace.db')
        conn.execute("""UPDATE Venue SET VenueCurr = VenueCurr + 1
                        WHERE VenueName=?""", (Venue,))
        conn.commit()
        conn.close()

        return "You have signed in successfully."

@app.route("/signout/", methods=["GET", "POST"])
def signout():
    if request.method == "GET":
        return render_template("signout.html")
    else:
        MatricNo, Venue = request.form["MatricNo"], request.form["venue"]
        x = datetime.datetime.now()
        time = x.strftime("%X")
        date = x.strftime("%x")

        # update time out in Entry
        conn = sqlite3.connect("studyspace.db")
        conn.execute("""UPDATE Entry SET TimeOut=?
                        WHERE date=? 
                        AND TimeOut= "NULL"
                        AND MatricNo=?""", (time, date, MatricNo))
        conn.commit()
        conn.close()

        # update venue capacity
        conn = sqlite3.connect('studyspace.db')
        conn.execute("""UPDATE Venue SET VenueCurr = VenueCurr - 1
                        WHERE VenueName=?""", (Venue,))
        conn.commit()
        conn.close()

        return "You have signed out successfully."

if __name__ == "__main__":
    app.run(debug=True)
