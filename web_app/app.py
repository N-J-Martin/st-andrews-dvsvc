from flask import Flask, request, render_template, redirect, url_for
import queries
app = Flask(__name__)
@app.route("/", methods = ['POST','GET'])
def location_filter():
    if request.method == "POST":
        current_loc = request.form["loc"]
        current_dist = request.form["dist"]
        nearby = queries.getLocations(current_loc, int(current_dist))
        return f"<p>{nearby}</p>"

    return render_template("index.html")
