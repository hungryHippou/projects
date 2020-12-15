from flask import Flask, render_template, url_for, request

app = Flask("__name__")

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/math/")
def math():
    return render_template("math.html")

@app.route("/physics/")
def physics():
    return render_template("physics.html")

@app.route("/econs/")
def econs():
    return render_template("econs.html")

@app.route("/computing/")
def computing():
    return render_template("computing.html")

if __name__ == "__main__":
    app.run(debug=False)
    
