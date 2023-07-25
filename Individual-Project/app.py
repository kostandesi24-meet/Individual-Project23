from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyApPMEEekkBsQ7FMvak7GAORWk8XXOMRqk",
  "authDomain": "peroject-b4214.firebaseapp.com",
  "projectId": "peroject-b4214",
  "storageBucket": "peroject-b4214.appspot.com",
  "messagingSenderId": "201962213422",
  "appId": "1:201962213422:web:b89fc7d733abf1c1654fbf",
  "measurementId": "G-C4K8VS8BSE" , 
  "databaseURL": "https://peroject-b4214-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

# signin
@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method=='POST':
        try: 
            login_session['user']=auth.sign_in_with_email_and_password(request.form['email'] ,request.form['password'])
            return redirect(url_for('homep'))        
        except:
            error="auth error"
    return render_template("login.html" , error = error)

# signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error= ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(request.form['email'] ,request.form['password'])
            uid=login_session['user']['localId']
            
            user = {"email": email,
            "password": password,
            "username": username}
            db.child('Users').child(uid).set(user)
            return redirect(url_for('homep'))
        except:
            error = "auth error"
    return render_template("signup.html" , error = error)

# signout
@app.route('/signout' , methods=['GET','POST'])
def signout():
    login_session['user']=""
    return redirect(url_for('login'))


@app.route('/homep' , methods=['GET','POST'])
def homep():
    if request.method == "POST":
        iid = request.form['img_id'] # ID of chosen img

        voted_img = db.child('Votes').child(iid).get().val()
        voted_img["votes"] = voted_img["votes"] + 1 # Getting and adding 1 to the vote for the chosen img

        final_vote = {"votes":voted_img["votes"]} # Updated vote count from previous lines

        db.child('Votes').child(iid).update(final_vote)

    vote= db.child('Votes').get().val()
    if vote == None :
        return render_template('homep.html')
    return render_template("homep.html" , votes=vote)
    

@app.route('/create' , methods=['GET' ,'POST'])
def create():
    error = ""
    if request.method=='POST':
        subject=request.form['subject']
        name=request.form['fp']
        adress=request.form['adress']
        try:
            vote={
            'subject': subject ,
            'name' : name ,
            'adress': adress , 
            'votes' : 0
            }
            db.child('Votes').push(vote)
            return redirect(url_for('homep'))
        except:
            error = "something went wrong !"
    return render_template('create.html' , error = error)



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)