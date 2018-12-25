from flask import Flask,render_template,request
import random
import string
from models import session
import models
import time
app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template("login.html")
@app.route("/login",methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("password")
        all_users = session.query(models.Users).all()
        for user in all_users:
            if username == user.name:
                if int(pwd) == user.password:
                    return render_template("success.html",content = "登陆成功")
                else:
                    return render_template("success.html", content="密码错误")
            else:
                return render_template("success.html", content="用户名不存在")
@app.route('/logincode',methods=["POST","GET"])
def login_code():
    def get_x_code(x):
        letter = string.ascii_letters
        digit = string.digits
        code = letter + digit
        data = random.choices(code,k=x)
        str_data = ''
        for i in data:
            str_data +=i
        return str_data
    code_count = session.query(models.Code).filter(models.Code.expire_date - getTimeOClockOfToday() <= 3600 * 24 * 2).count()
    if code_count < 10:
        code = get_x_code(4)
        session.add(models.Code(code=code, expire_date=int(time.time()) + 60 * 60 * 24, is_register=0))
        session.commit()
        print(code)
        return render_template("code_page.html",code = "恭喜你获得注册码:"+code)
    else:
        return render_template("code_page.html",code = "今天验证码已经发放完毕")
@app.route("/to_register",methods=["GET"])
def to_register():
    return render_template('register.html')
@app.route("/register",methods=["POST"])
def register():
    username = request.form.get("username")[0:10]
    pwd = request.form.get("pwd")
    code = request.form.get("code")
    valid_codes = session.query(models.Code).filter(models.Code.expire_date-getTimeOClockOfToday()<=3600*48)
    list_code = []
    for valid in valid_codes:
        list_code.append(valid.code)
    if code not in list_code:
        print("验证码已过期/错误")
        return render_template('success.html',content = "注册码已过期/错误")
    else:
        for valid in valid_codes:
            if code == valid.code:
                if valid.is_register != 1:
                    all_users = session.query(models.Users.name).all()
                    list_user = []
                    for user in all_users:
                        list_user.append(user.name)
                    if username not in list_user:
                        session.add(models.Users(name = username,password = pwd))
                        session.query(models.Code).filter(models.Code.code==code).update({"is_register":1})
                        session.commit()
                        return render_template('success.html',content = "注册成功")
                    else:
                        return render_template('success.html',content = "用户名已存在")
                else:
                    return render_template('success.html',content = "验证码已注册")
def getTimeOClockOfToday():
    t = time.localtime(time.time())
    time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t),'%Y-%m-%d %H:%M:%S'))
    return int(time1)
if __name__ == '__main__':
    app.run()
