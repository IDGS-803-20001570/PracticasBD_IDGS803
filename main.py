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

@app.route("/eliminar",methods=["GET","POST"])
def eliminar():
    empleados_form=forms.EmpleadosForm(request.form)
    if request.method == 'GET':
        id=request.args.get('id')
        empleados1= db.session.query(Empleados).filter(Empleados.id==id).first()
        empleados_form.id.data = request.args.get('id')
        empleados_form.nombre.data=empleados1.nombre
        empleados_form.correo.data=empleados1.correo
        empleados_form.direccion.data=empleados1.direccion
        empleados_form.telefono.data=empleados1.telefono
        empleados_form.sueldo.data=empleados1.sueldo
    if request.method == 'POST':
        id=empleados_form.id.data
        emp = Empleados.query.get(id)
        db.session.delete(emp)
        db.session.commit()
        return redirect('ABC_Completo')
    return render_template("eliminar.html",form=empleados_form)

@app.route("/modificar",methods=["GET","POST"])
def modificar():
    empleados_form=forms.EmpleadosForm(request.form)
    if request.method == 'GET':
        id=request.args.get('id')
        empleado1= db.session.query(Empleados).filter(Empleados.id==id).first()
        empleados_form.id.data = request.args.get('id')
        empleados_form.nombre.data=empleado1.nombre
        empleados_form.correo.data=empleado1.correo
        empleados_form.telefono.data=empleado1.telefono
        empleados_form.direccion.data=empleado1.direccion
        empleados_form.sueldo.data=empleado1.sueldo
    if request.method == 'POST':
        id=empleados_form.id.data
        emp1= db.session.query(Empleados).filter(Empleados.id==id).first()
        emp1.nombre=empleados_form.nombre.data
        emp1.correo=empleados_form.correo.data
        emp1.telefono=empleados_form.telefono.data
        emp1.direccion=empleados_form.direccion.data
        emp1.sueldo=empleados_form.sueldo.data
        db.session.add(emp1)
        db.session.commit()
        return redirect('ABC_Completo')
    return render_template("modificar.html",form=empleados_form)


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()

