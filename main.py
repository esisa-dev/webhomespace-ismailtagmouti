from flask import Flask , render_template ,request 

from Login import login


log : login
pathcurent : str = ""
fixUsername : str = ""
app = Flask(__name__,template_folder="template",static_folder = 'static')

@app.route("/")
def accueil():
    return render_template("Login.html")


@app.route('/logout')
def lougout():
    return render_template("Login.html")
#Authentification
@app.route("/login",methods =["GET","POST"])
def home():
    global fixUsername
    global pathcurent
    username : str = request.form['username']
    password : str = request.form['password']
    log = login(username,password)
    if username != "" :
        if log.login() == True:   
            fixUsername = username
            pathcurent = "/home/"+username
            return render_template("home.html")
    return render_template("Login.html",erreur = "username or password incorrect ")

#Ajouter utilisateur
@app.route('/adduser',methods =["GET","POST"])
def createaccount():
    if request.method == 'GET':
        return render_template("AjouterUser.html")
    else :
        username : str = request.form['username']
        password : str = request.form['password']
        newpassword : str = request.form['repassword']
        log = login(username, password)
        if password != newpassword : 
            return render_template("AjouterUser.html",erreur = "password incorrect")
        if log.adduser() == False :
            print("x")
            return render_template("AjouterUser.html",erreur = "username already exists")
        return render_template("home.html")
if __name__ == '__main__':
    app.run()