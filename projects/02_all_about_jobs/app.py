from flask import Flask, render_template, request, redirect, send_file
from scrapper import remoteok, wework, indeed
from exporter import exporter

app = Flask("find_remote_jobs")

fake_db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report")
def report():
    job_keyword = request.args.get("job_keyword")

    if job_keyword:
        job_keyword = job_keyword.lower()
        existing_job = fake_db.get(job_keyword)

        if existing_job:
            jobs = existing_job
        else:
            jobs = remoteok.get_jobs(job_keyword) + wework.get_jobs(job_keyword) + indeed.get_jobs(job_keyword)
            fake_db[job_keyword] = jobs
    else:
        return redirect("/")

    return render_template(
        "report.html",
        jobKeyword = job_keyword,
        resultNum = len(jobs),
        jobs = jobs
    )

@app.route("/export")
def export():
    try:
        job_keyword = request.args.get("job_keyword")

        if not job_keyword:
            raise Exception()

        job_keyword = job_keyword.lower()
        jobs = fake_db.get(job_keyword)

        if not jobs:
            raise Exception()

        exporter.save_to_file(jobs)
        return send_file("jobs.csv")

    except:
        return redirect("/")


# app.run(host="0.0.0.0")