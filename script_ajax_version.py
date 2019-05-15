from flask import Flask, render_template, json, request, redirect, session, url_for
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from pathlib import Path


mysql = MySQL()
app = Flask(__name__)


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ar250562#'
app.config['MYSQL_DATABASE_DB'] = 'maintenance_app'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('sign_up_old.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('sign_up_old.html')
    _name = request.form['frm_usn']
    _email = request.form['frm_email']
    _password = request.form['frm_password']

    if _name and _email and _password:
            
        conn = mysql.connect()
        cursor = conn.cursor()
        _hashed_password = generate_password_hash(_password)
        query = "INSERT INTO `residents`(username, emailID, password) VALUES(%s,%s,%s)"
        args = (_name, _email, _password)
        cursor.execute(query, args)

        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'entry recorded successfully!'})
        else:
            return json.dumps({'error':str(data[0])})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})
    cursor.close()
    conn.close()

@app.route('/payment', methods=['GET','POST'])
def pay():
    if request.method == 'GET':
        return render_template('payment_page.html')
    conn = mysql.connect()
    cursor = conn.cursor()

    _name = request.form['frm_name']
    _flatno = request.form['frm_flatno']
    _purpose = request.form['frm_purpose']
    _payment_method = request.form['frm_payment_method']
    _payment_ref = request.form['frm_pay_ref']
    _amount = request.form['frm_amt']
    _year = request.form['frm_year']
    _month = request.form['frm_month']

    query = "SELECT residentID FROM residents WHERE name_=%s;"
    args = _name
    cursor.execute(query,args)
    for _residentID in cursor:
        pass


    query = 'INSERT INTO `payment_history`(flatno, residentID, date, amount, year, month, payment_method, bank, payment_ref, receipt_no, purpose)' \
            ' VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    args = (_flatno, *_residentID, datetime.today().strftime('%d-%m-%Y'), _amount, _year, _month, _payment_method, _bank,\ _payment_ref,'NULL' , _purpose)
    cursor.execute(query,args)
    data = []
    if len(data) is 0:
        conn.commit()
        #return json.dumps({'message':'entry recorded successfully!'})
        return redirect(url_for('get_data'))

    else:
        return json.dumps({'error':str(data[0])})

    cursor.close()
    conn.close()
@app.route('/payment_details', methods=['GET','POST'])
def get_data():
    data=[]
    conn = mysql.connect()
    cursor = conn.cursor()
    query = 'SELECT %s,%s,%s,%s,%s,%s,%s,%s FROM payment_history WHERE residentID=%s '

    args = (date, purpose, amount, month, year, payment_method, bank, payment_ref, receipt_no, *_residentID)
    cursor.execute(query,args)
    for x in cursor:
        data.append(x)
    print(data)
if __name__ == "__main__":
    app.run(port=5002)

