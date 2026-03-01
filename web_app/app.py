from flask import Flask, request, render_template, redirect, url_for
import queries
app = Flask(__name__)
@app.route("/", methods = ['POST','GET'])
def location_filter():
    if request.method == "POST":
        current_loc = request.form["loc"]
        current_dist = request.form["dist"]
        nearby = queries.getLocations(current_loc, int(current_dist))
        outstr = ""
        for l in nearby:
            outstr = outstr + f"<p>{l}</p>"

        if nearby == []:
            return "<h1>Error searching location</h1>"
        return outstr

    return render_template("index.html")
