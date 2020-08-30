from flask import Flask, render_template, url_for, redirect, request 



app = Flask(__name__)


subjects = ["H2 Subject 1", "H2 Subject 2", "H2 Subject 3", "H1 Subject", "General Paper", "Project Work", "Mother Tongue"]
grades = ["A", "B", "C", "D", "E", "S", "U"]
points = [20.00, 17.50, 15.00, 12.50, 10.00, 5.00, 0.00]


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/rp/", methods=["GET", "POST"])
def rp():
    if request.method == "GET":
        return render_template("rp.html") 
    else: 
        # read data
        pw, mt = request.form["PW"], request.form["MT"]
        chosen = subjects[:5] # default 
        
        if pw == "yes" and mt == "yes":
            chosen = subjects
        elif pw == "yes":
            chosen.append(subjects[5])
        elif mt == "yes":
            chosen.append(subjects[6])

        return render_template("rp2.html", chosen=chosen, grades=grades)

@app.route("/calculate/", methods=["POST"])
def calculate():
    if request.method == "POST":
        response = dict(request.form)
        chosen = list(response.keys())
        got = list(response.values())
        ranks = []
        total = 80.00
        actual = 0.00 

        if "Project Work" in chosen:
            total += 10.00

        for i in range(len(chosen)):
            for j in range(len(grades)):
                if got[i] == grades[j]:
                    temp = j
                    if i >= 3:
                        actual += points[temp] / 2
                        ranks.append(points[temp] / 2)
                    else: 
                        actual += points[temp]
                        ranks.append(points[temp])

        return render_template("calculate.html", chosen=chosen, got=got, ranks=ranks,
        total=total, actual=actual)

if __name__ == "__main__":
    app.run(debug=True)