from flask import Flask,render_template,request

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("keyword")
    okyo = {'okyo1':'色不異空','okyo2':'空不異色','okyo3':'色即是空','okyo4':'空即是色'}
    return render_template("index.html",passed_keyword=name,okyo=okyo)


@app.route("/hello",methods=["post"])
def post():
    name = request.form["name"]
    okyo = {'okyo1':'色不異空','okyo2':'空不異色','okyo3':'色即是空','okyo4':'空即是色'}
    return render_template("index.html", passed_keyword=name, okyo=okyo)

