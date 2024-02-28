from flask import Flask,render_template,request,Response
from flask_wtf.csrf import CSRFProtect
from flask import redirect
from flask import flash
from config import DevelopmentConfig
from flask import g

import forms
from models import db
from models import Empleados


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.route("/index",methods=["GET","POST"])
def index():
    empleados_form=forms.EmpleadosForm(request.form)
    if request.method == 'POST' and empleados_form.validate():
        empleados = Empleados(nombre=empleados_form.nombre.data,
                       correo=empleados_form.correo.data,
                       telefono = empleados_form.telefono.data,
                       direccion = empleados_form.direccion.data,
                       sueldo = empleados_form.sueldo.data)
        db.session.add(empleados)
        db.session.commit()
    return render_template("index.html",form=empleados_form)

@app.route("/ABC_Completo",methods=["GET","POST"])
def ABC_Completo():
    empleados_form=forms.EmpleadosForm(request.form)
    empleado = Empleados.query.all()
    return render_template("ABC_Completo.html",empleado=empleado)


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()

