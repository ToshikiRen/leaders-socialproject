from flask import Flask, render_template, request, redirect, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
import datetime
from flask_login import  LoginManager, UserMixin, login_user, login_required, current_user, logout_user
app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3003@localhost/MedBase'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://swxnqrtligtnbj:78bd21ec0a30820c6ef6eae5882e8ec22cc529a6e69e013147e5ab1c7644f4b4@ec2-3-234-109-123.compute-1.amazonaws.com:5432/d50i8gfcv8vabf'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

class Feedback(db.Model):

    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key = True)
    customer = db.Column(db.String(200), unique = True)
    dealer = db.Column(db.String(200), )
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


class New(UserMixin, db.Model):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(80), )

    def __init__(self, username, password):
        self.username = username
        self.password = password



@login_manager.user_loader
def load_user(user_id):
    return New.query.get(int(user_id))
# Asta e rulat prima data cand deschidem aplicatia
@app.route('/')
def index():
    # Add login.html, the after login go to index
    if current_user.is_authenticated:
        return redirect('/login_succes')
    return render_template('login.html')

#@app.route('/login', methods = ['POST'])
#def gotologin():
#    if request.method == 'POST':
#        return render_template('login.html') 

#Asta ruleaza cand dam submit datelor introduse in formular
@app.route('/submit', methods=['POST'])
@login_required
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
       
        if customer == '' or dealer == '':
            return render_template('index.html', message = 'Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html', message = 'You have already submited feedback')


# Asta ruleaza cand vrem sa ne conectam la aplicatie
@app.route('/login_succes', methods=['POST', 'GET'])
def login():
    #if request.method == 'POST':
    #TO DO: Adaugare verificare date logare
    if current_user.is_authenticated:
        return render_template('index.html')
    try:
        username = request.form['username']
    except:
        username = ''
    try:
        password = request.form['password']
    except:
        password = ''
    try:
        remember = request.form['remember']
    except:
        remember = ""
        
    if (db.session.query(New).filter(username == New.username).count() and
        db.session.query(New).filter(New.password == password).count()):
        if not remember:
            login_user(New.query.filter_by(username = username).first())
        else:
            login_user(New.query.filter_by(username = username).first(), remember=True)
        if remember:
            #expire_date = datetime.datetime.now()
            #expire_date = expire_date + datetime.timedelta(days=90)
            resp = make_response(render_template('index.html'))
            
            resp.set_cookie('username', username)
            resp.set_cookie('password', password)
            resp.set_cookie('remember', 'checked')

            return resp
        user = username
        return render_template('index.html')
    if username or password:
        return render_template('login.html', message = 'Date invalide')
    return render_template('login.html')

# Asta ruleaza cand apasam butonul Cautare Pacienti
@app.route('/querry')
@login_required
def querry():
    return render_template('querry_data.html');

# Asta ruleaza cand apasam pe Sign Up
@app.route('/signup', methods=['POST', 'GET'])
def gotosignin():
    return render_template('signup.html')

# Asta ruleaza cand daum submit datelor pentru creare cont nou
@app.route('/response', methods=['POST'])
def sigin():
    if request.method == 'POST':
        # De adaugat o functie de hashing pentru securizarea datelor
        username = request.form['username']
        password = request.form['password']
        cPassword = request.form['confirm_password']
        if db.session.query(New).filter(New.username == username).count() >= 1:
            return render_template('signup.html',  message = 'Username-ul este deja folosit de catre alt utilizator')
        if len(password) < 6:
            return render_template('signup.html',  message = 'Parola prea scurta')
        if password != cPassword:
            return render_template('signup.html', message = 'Cele doua parole nu sunt identice')
        if len(username) < 1:
            return render_template('signup.html', message = 'Introduceti un username')
        data = New(username, password)
        db.session.add(data)
        db.session.commit()
        return render_template('login.html',  message = 'Sign Up succesful')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()

    