from flask import Flask,render_template,request
from .models.models import OnegaiContent
from .models.database import db_session
from datetime import datetime

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("keyword")
    after = request.args.get("after")
    all_onegai = OnegaiContent.query.all()
    return render_template("index.html",passed_keyword=name,after=after,all_onegai=all_onegai)


@app.route("/hello",methods=["POST"])
def post():
    name = request.form["name"]
    all_onegai = OnegaiContent.query.all()
    return render_template("index.html", passed_keyword=name, all_onegai=all_onegai)


@app.route("/add",methods=["post"])
def add():
    name = request.form["name"]
    body = request.form["body"]
    content = OnegaiContent(name,body,datetime.now())
    db_session.add(content)
    db_session.commit()
    return index()


@app.route("/update",methods=["post"])
def update():
    content = OnegaiContent.query.filter_by(id=request.form["update"]).first()
    content.name = request.form["name"]
    content.body = request.form["body"]
    db_session.commit()
    return index()


@app.route("/done",methods=["post"])
def done():
    name = request.form["name"]
    body = request.form["body"]
    content = OnegaiContent(name,body,datetime.now())
    db_session.add(content)
    db_session.commit()
    return index


    

