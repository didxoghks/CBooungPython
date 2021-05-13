from flask import Flask, render_template, request
from WebScraper.WebMain.Scrapper import get_jobs

app = Flask("SupperScrapper")

DB = {}
@app.route("/")
def home():
    return render_template("potato.html")

@app.route("/contact")
def contact():
    return "contactable number 010-1234-1234"

@app.route("/<username>")
def potato(username):
    return f"Hello {username} how are you!"

@app.route("/제목")
def title():
    return "<h1> Job Search</h1>"

@app.route("/report")
def report():
    word = request.args.get('word')
    word = word.lower()
    fromDb = DB.get(word)
    if fromDb:
        jobs = fromDb
    else:
        jobs = get_jobs(word)
        DB[word] = jobs

    return render_template("potato.html", searchingBy = word, resultNumbers = len(jobs))



app.run(host="127.0.0.1")
