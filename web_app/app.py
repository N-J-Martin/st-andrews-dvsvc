from flask import Flask, request, render_template, redirect, url_for
import queries
app = Flask(__name__)
@app.route("/", methods = ['POST','GET'])
def location_filter():
    if request.method == "POST":
        current_loc = request.form["loc"]
        current_dist = request.form["dist"]
        nearby = queries.getLocations(current_loc, int(current_dist))
        outstr = f"""<head><link rel="stylesheet" href="{ url_for('static', filename='index.css')}"> </head> <body> <ul>"""
        for l in nearby:
            outstr = outstr + f"""<li onclick="location.href='{url_for('charity_page',name=l[0])}';", style="outline: thick inset"><div >
            <h3>{l[0]}</h3>
            <a href='{l[1]}'> {l[1]} </a>
            <br>
            <br>
            location: {l[3]}
            <br>
            phone number: {l[4]}
            <br>
            email: {l[5]}
            <br>
            <br>
            description: {l[2]}
            <br>

            </div></li>"""

        if nearby == []:
            return "<h1>Error searching location</h1>"
        return outstr+"</ul> </body>"

    return render_template("index.html")


@app.route("/charity/<name>")
def charity_page(name):
    page = f"""<head><link rel="stylesheet" href="{ url_for('static', filename='index.css') }">
</head>
<body> 
<h1>{name}</h1>"""
    charity_info = queries.get_charity_info_by_name(name)
    if charity_info == []:
        return "<h1>Unknown Charity </h1>"
    charity_info = charity_info[0]
    charity_details = f"""
    <div>
        <a href='{charity_info[0]}'> {charity_info[0]} </a>
        <br>
        <br>
        {charity_info[1]}
        <br>
        <br>
        Charity Number: {charity_info[2]}
    </div>
    """

    service_info = queries.getServicesByCharityName(name)
    service_details = "<h2>Services</h2><ul>"
    for s in service_info:
        print(s)
        service_details = service_details + f"""
                <li>
                <div style="outline: thick inset">
                    description: {s[0]}
                    <br>
                    <br>
                    location: {s[1]}
                    <br>
                    phone number: {s[3]}
                    <br>
                    email: {s[2]}
                    <br>
                    <br>
                </div>
                <br>
                </li>
        """
    page = page + charity_details + service_details+"</ul> </body>"
    return page
