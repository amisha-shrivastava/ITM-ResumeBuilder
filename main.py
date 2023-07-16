from flask import Flask,render_template,request,redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
import hashlib


app = Flask(__name__)
app.secret_key = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
db = SQLAlchemy(app)

class Register(db.Model):
    name = db.Column(db.String(20))
    roll_no = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20))
    mobile = db.Column(db.String(10))
    course = db.Column(db.String(20))
    year = db.Column(db.String(20))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    if 'username' in session:
        return render_template("home.html")
    else:
        return 'You are not logged in!'


@app.route('/resume_1')
def resume_1():
    return render_template("resume_1.html")

@app.route('/resume_2')
def resume_2():
    return render_template("resume_2.html")

@app.route('/resume_template')
def resume_template():
    return render_template("resume_template.html")




@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Register.query.filter_by(email=username, roll_no=password).first()
        if user:
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register',methods =['GET','POST'])
def register():
    if request.method == 'POST':
        'add entry to DB'
        name = request.form.get('fullname')
        roll_no = request.form.get('rollno')
        email = request.form.get('email')
        mobile = request.form.get('phone')
        course = request.form.get('course')
        year = request.form.get('year')


        insert = Register(name=name , roll_no=roll_no,email=email,mobile=mobile,course=course, year=year)
        db.session.add(insert)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html")


if(__name__ == "__main__"):
    app.run(debug=True)