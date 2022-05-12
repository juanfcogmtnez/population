from flask import Flask, jsonify, render_template, request, url_for, redirect, session, send_file
import pymongo
from html.parser import HTMLParser
from pymongo import MongoClient
from bson.json_util import dumps
from werkzeug.utils import secure_filename
import os, os.path
from datetime import date
import crea, bk
app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
app.config['UPLOAD_PATH'] = 'despl/ofertas'
app.secret_key = 'esto-es-una-clave-muy-secreta'
#app.register_blueprint(base,url_prefix='/base',template_folder='templates',static_folder='static')
#app.register_blueprint(proyectos,url_prefix='/proyectos',template_folder='templates',static_folder='static')
#app.register_blueprint(unidades,url_prefix='/unidades',template_folder='templates',static_folder='static')
#app.register_blueprint(rooms,url_prefix='/rooms',template_folder='templates',static_folder='static')
#app.register_blueprint(despl,url_prefix='/despl',template_folder='templates',static_folder='static')

@app.route("/")
def hello_world():
	consulta = crea.create_first()
	if consulta == "OK":
		return redirect(url_for('login'))
	else:
		return "la base de datos no se ha cargado correctamente"

@app.route('/upload', methods=['POST'])
def upload_files():
    item = request.form['item']
    marca = request.form['marca']
    modelo = request.form['modelo']
    precio = request.form['precio']
    calidad = request.form['calidad']
    ref_proyecto = request.form['ref_proyecto']
    today = date.today()
    fecha = today.strftime("%m/%Y")
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        try:
            os.makedirs(app.config['UPLOAD_PATH']+"/"+item+"/")
            print("Directory " , app.config['UPLOAD_PATH']+"/"+item+"/" ,  " Created ")
        except FileExistsError:
            print("Directory " , app.config['UPLOAD_PATH']+"/"+item+"/" ,  " already exists")
    contenido = os.listdir(app.config['UPLOAD_PATH']+"/"+item+"/")
    numero = len(contenido)
    print("numero:", numero)
    filename = item+"_"+str(numero)+".pdf"
    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH']+"/"+item+"/", filename))
    #mete aqui el read para guardar el registro, acuerdate de meter el numero y en el html la calidad
    registra = read.newrelo(item,marca,modelo,precio,ref_proyecto,fecha,numero,calidad)
    return redirect(url_for('despl.index'))

@app.route("/login", methods=["POST", "GET"])
def login(message=None):
    if message == None:
        message = 'Por favor introduce tus datos'
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        result = crea.checkpwd(email,pwd)
        print(result)
        if result != "Error":
            session['nombre'] = result[1]
            session['role'] = result[0]
            return render_template('pop.html')
        else:
            message='Contraseña incorrecta'
    return render_template('login.html', message=message)

@app.route("/register", methods=["POST", "GET"])
def register():
	message = ""
	script = ""
	if request.method == 'POST':
		nombre = request.form['nombre']
		email = request.form['email']
		role = 'user'
		p1 = request.form['password1']
		p2 = request.form['password2']
		message = crea.registro(nombre,email,role,p1,p2)
		if message == "Usuario creado, serás redirigido en cinco segundos":
			script = "redirect()"
	return render_template('register.html',message=message,script=script)

@app.route("/forget", methods=["POST", "GET"])
def forget():
    message = "Indica tu email"
    if request.method == 'POST':
        diremail = request.form['email']
        direccion = request.url.encode("utf-8")
        direccion = str(direccion)
        direccion = direccion[9:]
        pos = direccion.find("/")
        direccion = direccion[0:pos]
        direccion = direccion.encode("utf-8")
        print(diremail)
        print(direccion)
        envio = envia.send(diremail,direccion)
        if envio != "":
            message = envio
    return render_template('forget.html',message=message)

@app.route("/repwd/<email>", methods=["POST", "GET"])
def repwd(email):
	email = email[:-1]
	script = ""
	message = 'Selecciona una contraseña'
	if request.method == 'POST':
		p1 = request.form['password1']
		p2 = request.form['password2']
		message = crea.uppwd(email,p1,p2)
		if message == "La contraseña se ha actualizado con éxito":
			script = "redirect()"
	return render_template('repwd.html',email=email,message=message,script=script)

######### BACKEND ##############

@app.route("/countries", methods=["POST", "GET"])
def countries():
    set = bk.countries()
    return set

@app.route("/sel/<country>/<year>", methods=["POST", "GET"])
def sel(country,year):
    set = bk.sel(country,year)
    return set
@app.route("/pop/<country>", methods=["POST", "GET"])
def pop(country):
    set = bk.sel_pop(country)
    return set

@app.route("/pop_year/<country>/<year>", methods=["POST", "GET"])
def pop_year(country,year):
    set = bk.sel_pop_year(country,year)
    return set

if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)
