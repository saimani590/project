from flask import Flask,render_template,request,redirect,session,url_for,flash
import sqlite3
app = Flask(__name__)
app.secret_key = "590"
# --------------------------------indexpage---------------------------
@app.route('/')
def index():
      return render_template('index.html')

# --------------------------------registerpage---------------------------
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
# sqlite
        connection = sqlite3.connect("app_data.db")
        cursor = connection.cursor()

#Html form
        name=request.form['name']
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirmpassword=request.form['confirmpassword']
        data=[name,username,email,password,confirmpassword]
        #print(name,username,email,password,confirmpassword)

#login authentications

        query1="SELECT username FROM registerdata WHERE username='"+username+"'"
        cursor.execute(query1)
        results = cursor.fetchall()
        if len(results) != 0:
            return "user already exists"
        else:

#register data insert

            query="INSERT INTO registerdata(name,username,email,password,confirmpassword) VALUES (?,?,?,?,?)"
            cursor.execute(query,data)
            connection.commit()
            # flash("register success",'info')
            return redirect('/login')
    return render_template('register.html')

# --------------------------------loginpage---------------------------
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
# sqlite
        connection = sqlite3.connect("app_data.db")
        cursor = connection.cursor()

#Html form
        username=request.form['namelogin']
        password=request.form['passwordlogin']

       # print(username,password)
#query
        query = "SELECT username,password FROM registerdata where username='"+username+"' and password='"+password+"'"
        cursor.execute(query)

        results = cursor.fetchall()
#validation
        if len(results) == 0:
            return "userid and password is incorrect"
        else:
             session['user'] = username
             return redirect(url_for("home"))
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template('login.html')

# --------------------------------homepage---------------------------
@app.route('/home')
def home():
    if 'user' in session:
        user = session['user']
        return render_template('home.html')
    else:
      return redirect(url_for("login"))

# --------------------------------logoutpage---------------------------
@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for("index"))

# @app.route('/alert')
# def alert():
#     # return "<html><head><script>alert('register successfully')</script></head></html>"
#     return redirect(url_for("register"))
#     # return render_template('alertmessage.html')
if __name__ == '__main__':
    app.run(debug=True)