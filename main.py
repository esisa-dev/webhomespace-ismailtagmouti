from flask import Flask , render_template ,request , send_file

from Login import login
from GestionHome import GestionHome
import os

authi : login
gsFiledr = GestionHome()
pathcurent : str = ""
fixUsername : str = ""

app = Flask(__name__,template_folder="template",static_folder = 'static')

#Envoyer l'utilisateur a la page d'authentification
@app.route("/")
def accueil():
    return render_template("Login.html")

@app.route('/logout')
def lougout():
    return render_template("Login.html")

#Authentification
@app.route("/auth",methods =["GET","POST"])
def home():
    global fixUsername
    global pathcurent
    username : str = request.form['username'] 
    password : str = request.form['password']
    authi = login(username,password)
    if username != "" :
        if authi.login() == True:   
            fixUsername = username
            pathcurent = "/home/"+username
            return render_template("home.html",directory = gsFiledr.getPath("/home/"+username) )
    return render_template("Login.html",erreur = "username or password incorrect ")

#Ajouter utilisateur
@app.route('/adduser',methods =["GET","POST"])
def createaccpunt():
    if request.method == 'GET':
        return render_template("AjouterUser.html")
    else :
        username : str = request.form['username']
        password : str = request.form['password']
        repassword : str = request.form['repassword']
        if password != repassword : 
            return render_template("AjouterUser.html",erreur = "password incorrect")
        if login.adduser(username,password) == False :
            return render_template("AjouterUser.html",erreur = "username already exists")
        return render_template("home.html",directory = gsFiledr.getPath("/home/"+username))
    
#Naviger sur les dossiers les fichiers 
@app.route('/<path:path>/',methods =["GET"])
def routefolders(path):
    try :
        global pathcurent
        pathcurent = "/"+path
        if os.path.isdir(pathcurent):
            return render_template("home.html",directory = gsFiledr.getPath(pathcurent))
        elif os.path.isfile(pathcurent):
            f = open(pathcurent)
            return render_template("home.html",text = f.read())
    except :
        return "erreur"


@app.route('/back',methods =["GET","POST"])
def back():
    global pathcurent
    t = pathcurent.split("/")
    if len(t) != 3 :
        pathcurent = ""
        for i in range(len(t)-1):
            pathcurent += t[i] + "/"
        pathcurent = pathcurent[:len(pathcurent)-1]
  
    if os.path.isdir(pathcurent):
       return render_template("home.html",directory = gsFiledr.getPath(pathcurent))

#Télecharger le home directory
@app.route("/download")
def download():
    gsFiledr.telechercherHomeDerectory(fixUsername)
    return send_file("/home/"+fixUsername+"/"+fixUsername+".zip", as_attachment=True)

#Retourner le nombre des fichiers
@app.route('/nbrfiles')
def nbrfiles():
    return render_template("home.html",directory = gsFiledr.getPath(pathcurent),fil = str(gsFiledr.getnbrFichier(pathcurent)))

#Retourner le nombre des dossiers
@app.route('/nbrdir')
def nbrdirs():
    return render_template("home.html",directory = gsFiledr.getPath(pathcurent),dir = str(gsFiledr.getnbrDirectory(pathcurent)))

#Retourner la taille d'un dossiers
@app.route('/space')
def space():
    return render_template("home.html",directory = gsFiledr.getPath(pathcurent),spa = str(gsFiledr.gettaille(pathcurent)))

#REchercher un file nom ou extention
@app.route('/findfile',methods =["GET","POST"])
def fileSearch():
    filename : str = request.form['file']
    return render_template("home.html",directory = gsFiledr.rechercheFilesNameFileExtention(pathcurent,filename))

if __name__ == '__main__':
    app.run()