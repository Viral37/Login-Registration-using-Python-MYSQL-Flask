from flask import Flask, render_template, request, session, redirect, url_for, flash
import MySQLdb
import os
from wtforms import Form, TextField, validators, TextAreaField
from werkzeug import secure_filename  
from werkzeug.utils import secure_filename  
app = Flask(__name__)
app.secret_key = "This is secrect key line"
app.config['UPLOAD_FOLDER'] = 'static/image/'

@app.route('/')
def homepage():
    try:
        if 'username' in session:
            username = session['username']
            # msg = "welcome "
            return render_template("index.html",session=session['username'])
        else:
             return render_template("index.html")
    except Exception as e:
        raise (str(e))

@app.route('/register', methods = ["GET", "POST"])
def register():
    try:
        if 'username' in session:
            username = session['username']
            msg = "Login User Can't Register Agian..."
            return render_template("register.html",msg=msg,session=session['username'])
        else:
             return render_template("register.html")
    except Exception as e:
        raise (str(e))

#************ use for rigister user ***************** 
@app.route('/sinup', methods=["GET", "POST"])
def sinup():
    try:
        db =MySQLdb.connect(host="localhost", user="root", passwd="root", db="user")
        cursor = db.cursor()
        x = cursor.execute("select * from users where email=%s",
                           (request.form['email']))
        if x > 0:
            return("This UserName Already registered, Please register again...")
            return render_template("registerpage.html")
        else:
            sql = "insert into users (name,gender, email,password,cpass,image) values (%s, %s, %s, %s, %s,%s)"
            ff = request.files['img']
            f = os.path.join(app.config['UPLOAD_FOLDER'], ff.filename)
            print(f)

            ff.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ff.filename)))

            da = (request.form['name'], request.form['gender'], request.form['email'], request.form['pass'], request.form['cpass'], f)
            number_of_rows = cursor.execute(sql, da)
            db.commit()
            db.close()
            return render_template("index.html")
    except Exception as e:
        return (str(e))

@app.route('/login')
def log():
    try:
        if 'username' in session:
            username = session['username']
            msg = "you Have Alwaredy Login in system go back to home page..! "
            return render_template("login.html",msg=msg,session=session['username'])
        else:
             return render_template("login.html")
    except Exception as e:
        raise (str(e))

    # return render_template('login.html')
# *******************************for login user* ***********************
@app.route('/', methods=["GET","POST"])
def login():
    try:
        db =MySQLdb.connect(host="localhost", user="root", passwd="root", db="user")
        cursor = db.cursor()
        sql = "select * from users where email =%s and password=%s"
        email = request.form['email']
        da = (request.form['email'],request.form['pass'])
        number_of_rows = cursor.execute(sql, da)

        count = cursor.fetchone()

        if count > 0:
            session['username'] = count[3]
            print "ss",session['username']
            return redirect(url_for('homepage'))
        else:
            sql = "select * from admin where email =%s and password=%s"
            da = (request.form['email'],request.form['pass'])
            number_of_rows = cursor.execute(sql, da)
            count = cursor.fetchone()
            if count > 0:
                session['username'] = count
                print "saaa",session['username']
                # sd = "select * from user where email=%s"

                return redirect(url_for('homepage'), session=session)
                print dat
                db.close()

            else:
                msg = "Sorry No Data Found"
                return render_template("login.html",msg=msg)

    except Exception as e:
        return (str(e))
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('homepage'))

@app.route('/about')
def about():
    return render_template("aboutus.html")
@app.route('/footer')
def footer():
    return render_template("footer.html")
@app.route('/test')
def test():
    try:
        db =MySQLdb.connect(host="localhost", user="root", passwd="root", db="user")
        cursor = db.cursor()
        query = "select * from users"
        rows = cursor.execute(query)
        data1 = cursor.fetchall()
        return render_template("testing.html",data1=data1)        
    except Exception as e:
        raise
# image uploade demo
@app.route('/upload', methods=["GET","POST"])
def upload():
    if request.method == 'POST':
      f = request.files['file']
      # print(os.getcwd())
      # os.chdir('/static/image/')
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      return 'file uploaded successfully'

if __name__ == "__main__":
    app.run(debug="True")