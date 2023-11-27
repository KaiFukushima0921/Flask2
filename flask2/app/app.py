from flask import Flask,render_template,request
from .models.models import OnegaiContent

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("keyword")
    after = request.args.get("after")
    all_onegai = OnegaiContent.query.all()
    return render_template("index.html",passed_keyword=name,after=after,all_onegai=all_onegai)


@app.route("/hello",methods=["post"])
def post():
    name = request.form["name"]
    all_onegai = OnegaiContent.query.all()
    return render_template("index.html", passed_keyword=name, all_onegai=all_onegai)


    

