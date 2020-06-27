from flask import Flask, render_template, request, redirect, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3003@localhost/MedBase'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://swxnqrtligtnbj:78bd21ec0a30820c6ef6eae5882e8ec22cc529a6e69e013147e5ab1c7644f4b4@ec2-3-234-109-123.compute-1.amazonaws.com:5432/d50i8gfcv8vabf'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


class New(db.Model):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(200), )

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
# Asta e rulat prima data cand deschidem aplicatia
@app.route('/')
def index():
    # Add login.html, the after login go to index
    return render_template('login.html')

#@app.route('/login', methods = ['POST'])
#def gotologin():
#    if request.method == 'POST':
#        return render_template('login.html') 

#Asta ruleaza cand dam submit datelor introduse in formular
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message = 'Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            #send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
    return render_template('index.html', message = 'You have already submited feedback')


# Asta ruleaza cand vrem sa ne conectam la aplicatie
@app.route('/login_succes', methods=['POST'])
def login():
    if request.method == 'POST':
        #TO DO: Adaugare verificare date logare
        username = request.form['username']
        password = request.form['password']
        remember = request.form['remember']
      
        if (db.session.query(New).filter(New.username == username).count() and
            db.session.query(New).filter(New.password == password).count()):
            #if remember:
            #    resp = make_response(redirect('/login_succes'))
            #    resp.set_cookie('username', username)
            #    resp.set_cookie('password', password)
            #    resp.set_cookie('remember', 'checked')

            #    return resp
            return render_template('index.html', message = 'Debug MSG')
        return render_template('login.html', message = 'Date invalide')

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

if __name__ == '__main__':
    app.run()

    