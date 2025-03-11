from flask import Flask, render_template, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig

import forms
from flask import request
from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/", methods=['GET','POST'])
@app.route("/index")
def index():
    create_form = forms.UserForm2(request.form)
    alumnos_list = Alumnos.query.all()  # Renamed variable to avoid conflict
    return render_template("index.html", form=create_form, Alumnos=alumnos_list)

@app.route("/Alumnos1", methods=['GET','POST'])
def Alumnos_view():
    create_form = forms.UserForm2(request.form)
    if request.method == 'POST':
        alumno = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            email=create_form.email.data
        )
        db.session.add(alumno)
        db.session.commit()
        flash('Alumnos registrado correctamente')
        return redirect(url_for('index'))
    return render_template("Alumnos.html", form=create_form)


@app.route("/detalles", methods=["GET", "POST"])
def detalles():
	create_forms=forms.UserForm2(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		Alumnos=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		nom=Alumnos.nombre
		ape=Alumnos.apaterno
		mail=Alumnos.email
		return render_template("detalles.html", form=create_forms, nom=nom, ape=ape, mail=mail)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
	create_forms=forms.UserForm2(request.form)
	if request.method == 'POST':
		Alumnos=Alumnos(nombre=create_forms.nombre.data,
				apaterno=create_forms.apaterno.data,
			    email=create_forms.email.data)
		#insertar Alumnos
		db.session.add(Alumnos)
		db.session.commit()
		flash("Alumnos agregado correctamente")
		return redirect(url_for("index"))
	return render_template("agregar.html", form=create_forms)
	
@app.route("/editar", methods=["GET", "POST"])
def editar():
	create_forms=forms.UserForm2(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		Alumnos=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_forms.id.data=request.args.get('id')
		create_forms.nombre.data=str.rstrip(Alumnos.nombre)
		create_forms.apaterno.data=Alumnos.apaterno
		create_forms.email.data=Alumnos.email
	if request.method == 'POST':
		id=create_forms.id.data
		Alumnos=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		Alumnos.nombre=str.rstrip(create_forms.nombre.data)
		Alumnos.apaterno=create_forms.apaterno.data
		Alumnos.email=create_forms.email.data
		db.session.add(Alumnos)
		db.session.commit()
		flash("Alumnos actualizado correctamente")
		return redirect(url_for("index"))
	return render_template("editar.html", form=create_forms)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_forms = forms.UserForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        Alumnos = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_forms.id.data = request.args.get('id')
        create_forms.nombre.data = Alumnos.nombre
        create_forms.apaterno.data = Alumnos.apaterno
        create_forms.email.data = Alumnos.email
    if request.method == 'POST':
        id = create_forms.id.data
        Alumnos = Alumnos.query.get(id)
        db.session.delete(Alumnos)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("eliminar.html", form=create_forms)


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()