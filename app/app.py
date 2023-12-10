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
    done = request.args.get("done")
    if after:
        all_onegai = OnegaiContent.query.filter(OnegaiContent.date>=after).all()
    elif done:
        all_onegai = OnegaiContent.query.filter(OnegaiContent.done==1).all()
    else:
        all_onegai = OnegaiContent.query.all()
    return render_template("index.html",passed_keyword=name,all_onegai=all_onegai)

"""
SQL文で書いた場合
select * from task where date >= after 
"""


""""
なぜ下記ではdoneカラムが1の値のみを表示出来ないのか？
"""

# @app.route("/")
# @app.route("/index")
# def index2():
#     name = request.args.get("keyword")
#     done = request.args.get("done")
#     if done:
#         all_onegai = OnegaiContent.query.filter(OnegaiContent.done==1).all()
#     else:
#         all_onegai = OnegaiContent.query.all()
#     return render_template("index.html",passed_keyword=name,all_onegai=all_onegai)


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


@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = OnegaiContent.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return index()


@app.route("/done",methods=["post"])
def done():
    done_list = request.form.getlist("done")
    for done in done_list:
        content = OnegaiContent.query.filter_by(id=done).first()
        content.done = True
        # 67行目は「done = 1」でも実行できた
        db_session.commit()
    return index()


# @app.route("/done",methods=["post"])
# def done():
#     name = request.form["name"]
#     body = request.form["body"]
#     content = OnegaiContent(name,body,datetime.now())
#     db_session.add(content)
#     db_session.commit()
#     return index


    

