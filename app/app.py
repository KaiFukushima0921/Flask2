from flask import Flask,render_template,request,session,redirect,url_for
from app import key
from hashlib import sha256
from .models.models import OnegaiContent,User
from .models.database import db_session
from datetime import datetime

app = Flask(__name__)
app.secret_key = key.SECRET_KEY


@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("keyword")
    after = request.args.get("after")
    done = request.args.get("done")
    if "user_name" in session:
        name = session["user_name"]
        all_onegai = OnegaiContent.query.all()
        return render_template("index.html",passed_keyword=name,all_onegai=all_onegai)
    elif after:
        all_onegai = OnegaiContent.query.filter(OnegaiContent.date>=after).all()
    elif done:
        all_onegai = OnegaiContent.query.filter(OnegaiContent.done==1).all()
    else:
        return redirect(url_for("top",status="logout"))

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


@app.route("/add",methods=["post"])
def add():
    name = request.form["name"]
    body = request.form["body"]
    content = OnegaiContent(name,body,datetime.now())
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("index"))


@app.route("/update",methods=["post"])
def update():
    content = OnegaiContent.query.filter_by(id=request.form["update"]).first()
    content.name = request.form["name"]
    content.body = request.form["body"]
    db_session.commit()
    return redirect(url_for("index"))


@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = OnegaiContent.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return redirect(url_for("index"))


@app.route("/done",methods=["post"])
def done():
    done_list = request.form.getlist("done")
    for done in done_list:
        content = OnegaiContent.query.filter_by(id=done).first()
        content.done = True
        # 67行目は「done = 1」でも実行できた
        db_session.commit()
    return redirect(url_for("index"))


@app.route("/login", methods=["post"])
def logion():
    email = request.form["user_name"]
    user = User.query.filter_by(user_name=email).first()
    if user:
        password = request.form["password"]
        hashed_password = sha256((email + password + key.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            session["user_name"] = email
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top",status="wrong_password"))
    else:
        return redirect(url_for("top",status="user_notfound"))
    

@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top",status="logout"))
    

@app.route("/resister",methods=["post"])
def resister():
    email = request.form["user_name"]
    user = User.query.filter_by(user_name=email).first()
    if user:
        return redirect(url_for("newcomer", status="exist_user"))
    else:
        password = request.form["password"]
        hashed_password = sha256((email + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(email, hashed_password)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = email
        return redirect(url_for("index"))
    

@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)


@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html",status=status)


    

