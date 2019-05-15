from flask import Flask, render_template, json, request, session, jsonify, redirect, url_for
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from pathlib import Path
import psycopg2
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class payment_history(db.Model):
    __tablename__ = 'payment_history'

    paymentID = db.Column(db.Integer, primary_key=True)
    flatno = db.Column(db.String())
    residentID = db.Column(db.Integer())
    amount = db.Column(db.Float())
    year = db.Column(db.Integer())
    month = db.Column(db.String())
    payment_method = db.Column(db.String())
    payment_ref = db.Column(db.String())
    receipt_no = db.Column(db.String())
    purpose = db.Column(db.String())

    def __init__(self, flatno, residentID, amount, year, month, payment_method, payment_ref, receipt_no, purpose):
        self.flatno = flatno
        self.residentID = residentID
        self.amount = amount
        self.year = year
        self.month = month
        self.payment_method = payment_method
        self.payment_ref = payment_ref
        self.receipt_no = receipt_no
        self.purpose = purpose

    def __repr__(self):
        return '<paymentID {}>'.format(self.paymentID)

    def serialize(self):
        return {
            'paymentID': self.paymentID,
            'flatno': self.flatno,
            'residentID': self.residentID,
            'amount': self.amount,
            'year': self.year,
            'month': self.month,
            'payment_method':self.payment_method,
            'payment_ref': self.payment_ref,
            'receipt_no':self.receipt_no,
            'purpose': self.purpose
        }
class residents(db.Model):
    __tablename__ = 'residents'

    residentID = db.Column(db.Integer, primary_key=True)
    name_ = db.Column(db.String())
    username = db.Column(db.String())
    emailID = db.Column(db.String())
    password = db.Column(db.String())
    mobno = db.Column(db.String())
    phno = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    country = db.Column(db.String())
    active = db.Column(db.String())
    owner = db.Column(db.String())
    role = db.Column(db.String())

    def __init__(self, name_, username, emailID, password, mobno, phno, city, state, country, active, owner, role):
        self.name_ = name_
        self.username = username
        self.emailID = emailID
        self.password = password
        self.mobno = mobno
        self.phno = phno
        self.city = city
        self.country = country
        self.active = active
        self.owner = owner
        self.role = role

    def __repr__(self):
        return '<residentID {}>'.format(self.residentID)

    def serialize(self):
        return{
            'residentID': self.residentID,
            'name_': self.name_,
            'username': self.username,
            'emailID': self.emailID,
            'password': self.password,
            'mobno': self.mobno,
            'ative': self.active,
            'owner': self.owner,
            'role': self.role
        }


@app.route('/')
def main():
    return render_template('sign_up.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        _name = request.form['frm_usn']
        _email = request.form['frm_email']
        _password = request.form['frm_password']

        if _name and _email and _password:
            _hashed_password = generate_password_hash(_password)
            data = []
            if len(data) is 0:
                return render_template('edit resident.html')
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    else:
        return render_template('sign_up.html')

@app.route("/getpay")
def get_pay():
    try:
        app = payment_history.query.all()
        return render_template('payment_details_page.html', data=app)
    except Exception as e:
        return (str(e))

@app.route('/payment', methods=['GET', 'POST'])

def payment():
    if request.method == "POST":
        name_ = request.form['frm_name']
        flatno = request.form['frm_flatno']
        purpose = request.form['frm_purpose']
        payment_method = request.form['frm_payment_method']
        payment_ref = request.form['frm_pay_ref']
        amount = request.form['frm_amt']
        year = request.form['frm_year']
        month = request.form['frm_month']

        resident = residents.query.filter_by(name_=name_).all()
        print(resident)
        residentID = resident.residentID

        try:
            payment_history = payment_history(
                flatno=flatno,
                residentID=residentID,
                amount=amount,
                year=year,
                month=month,
                payment_method=payment_method,
                payment_ref=payment_ref,
                receipt_no=receipt_no,
                purpose=purpose,
            )
            db.session.add(payment_history)
            db.session.commit()
            return redirect(url_for('get_pay'))
        except Exception as e:
            return (str(e))
        return render_template("payment_details_list.html")
    else:
        return render_template("payment_page.html")








if __name__ == "__main__":
    app.run(port=5002)
