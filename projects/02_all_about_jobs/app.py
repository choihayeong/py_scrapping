# from os import sendfile
from flask import Flask, redirect, render_template, request, send_file
from scrapping import get_jobs
from exporter import save_to_file

app = Flask(__name__)

fake_db = {}

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/report')
def contact():
    keyword = request.args.get("keyword")

    if keyword:
        keyword = keyword.lower()
        existingJobs = fake_db.get(keyword)

        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(keyword)
            fake_db[keyword] = jobs
    else:
        return redirect("/")
        # return render_template("home.html")

    return render_template(
        "report.html",
        searchingBy = keyword,
        resultsNum = len(jobs),
        jobs = jobs
    )

@app.route("/export")
def export():
    try:
        keyword = request.args.get("keyword")

        if not keyword:
            raise Exception()

        keyword = keyword.lower()
        jobs = fake_db.get(keyword)

        if not jobs:
            raise Exception()

        save_to_file(jobs)
        return send_file("your_jobs.csv", as_attachment=True)

    except:
        return redirect("/")

# app.run(host='0.0.0.0')