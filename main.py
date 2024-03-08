from flask import Flask,render_template,request,Response
from sqlalchemy import update
from flask_wtf.csrf import CSRFProtect
from flask import redirect
from flask import flash
from config import DevelopmentConfig
from flask import g

import forms
from models import db
from models import Empleados
from models import PedidosPizza
from models import VentasPizzas
from datetime import date


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

ingredientesDiccionario = {
    '1': 'Jamon',
    '2': 'Piña',
    '3': 'Champiñones'
}
tamañoDiccionario = {
    '40': 'Chica',
    '80': 'Mediana',
    '120': 'Grande'
}

mismaVenta = True
nombreCliente = ""
direccionCliente = ""
telefonoCliente = ""

@app.route("/pizzeria",methods=["GET","POST"])
def pizzeria():
    global mismaVenta
    global nombreCliente
    global direccionCliente
    global telefonoCliente

    pizzeria_form=forms.PizzeriaForm(request.form)
    formFecha = forms.ConsultaPedidosForm(request.form)
    pedidosPiza = PedidosPizza.query.filter_by(estatus=1).all()
    # pedidosPiza = PedidosPizza.query.all()

    if request.method == 'POST' and pizzeria_form.validate():
        costoPizza = int(pizzeria_form.tamaPizza.data)
        #ingrePizza = int(pizzeria_form.ingredientesPizza.data)
        totalPizza = int(pizzeria_form.numPizzas.data)
        subtotalPizza = str( (costoPizza+10)*totalPizza )
        totalPizza = "0"
        
        numVenta = db.session.query(db.func.max(PedidosPizza.numeroVenta)).scalar()
        if numVenta is None:
            numVenta = 1
            # print("--------------------------------------------------------1")
        elif mismaVenta:
            # print("--------------------------------------------------------2")
            nombreCliente = pizzeria_form.nombre.data
            direccionCliente = pizzeria_form.direccion.data
            telefonoCliente = pizzeria_form.telefono.data

            pizzeria_form.nombre.data = nombreCliente
            pizzeria_form.direccion.data = direccionCliente
            pizzeria_form.telefono.data = telefonoCliente

            pizzeria_form.nombre.render_kw = {'readonly': True}
            pizzeria_form.direccion.render_kw = {'readonly': True}
            pizzeria_form.telefono.render_kw = {'readonly': True}
            pass
        else:
            # print("--------------------------------------------------------3")
            numVenta = str(int(numVenta)+1)
            pizzeria_form.nombre.render_kw = {'readonly': False}
            pizzeria_form.direccion.render_kw = {'readonly': False}
            pizzeria_form.telefono.render_kw = {'readonly': False}
            mismaVenta = True                

        # print("------------------------------------------Num Venta: {}".format(numVenta))
        nuevo_pedido = PedidosPizza(
            nombre=pizzeria_form.nombre.data,
            direccion=pizzeria_form.direccion.data,
            telefono=pizzeria_form.telefono.data,
            tamaPizza=pizzeria_form.tamaPizza.data,
            ingredientesPizza= pizzeria_form.ingredientesPizza.data,
            numPizza=pizzeria_form.numPizzas.data,
            subtotal=subtotalPizza,
            total=totalPizza,
            numeroVenta = numVenta,
            estatus = "1"
        )
        db.session.add(nuevo_pedido)
        db.session.commit()
        pedidosPiza = PedidosPizza.query.filter_by(estatus=1).all()
        for pedido in pedidosPiza:
            pedido.ingredientesPizza = ingredientesDiccionario[pedido.ingredientesPizza]
            pedido.tamaPizza = tamañoDiccionario[pedido.tamaPizza]

        return render_template("pizzeria.html",pedidos=pedidosPiza,form=pizzeria_form, formF=formFecha)
        
    fecha_seleccionada = formFecha.fecha_seleccionada.data
    if not fecha_seleccionada: 
        fecha_seleccionada = date.today()  
    ventasFecha = db.session.query(VentasPizzas.nombre, db.func.sum(VentasPizzas.total).label('total')).filter(VentasPizzas.create_date == fecha_seleccionada).group_by(VentasPizzas.nombre).all()
      
    for pedido in pedidosPiza:
        pedido.ingredientesPizza = ingredientesDiccionario[pedido.ingredientesPizza]
        pedido.tamaPizza = tamañoDiccionario[pedido.tamaPizza] 

    return render_template("pizzeria.html",pedidos=pedidosPiza,form=pizzeria_form,formF=formFecha,ventasFecha=ventasFecha)

@app.route("/modificarPedido",methods=["GET","POST"])
def modificarPedido():
    pizzeria_form=forms.PizzeriaForm(request.form)
    if request.method == 'GET':
        id=request.args.get('id')
        pedidoPizza= db.session.query(PedidosPizza).filter(PedidosPizza.id==id).first()
        pizzeria_form.id.data = request.args.get('id')
        pizzeria_form.nombre.data=pedidoPizza.nombre
        pizzeria_form.direccion.data=pedidoPizza.direccion
        pizzeria_form.telefono.data=pedidoPizza.telefono        
        pizzeria_form.tamaPizza.data=pedidoPizza.tamaPizza
        pizzeria_form.ingredientesPizza.data=pedidoPizza.ingredientesPizza
        pizzeria_form.numPizzas.data=pedidoPizza.numPizza
    if request.method == 'POST':
        id=pizzeria_form.id.data
        pedidoPizza1= db.session.query(PedidosPizza).filter(PedidosPizza.id==id).first()
        pedidoPizza1.nombre=pizzeria_form.nombre.data
        pedidoPizza1.direccion=pizzeria_form.direccion.data
        pedidoPizza1.telefono=pizzeria_form.telefono.data
        pedidoPizza1.tamaPizza =pizzeria_form.tamaPizza.data
        pedidoPizza1.ingredientesPizza=pizzeria_form.ingredientesPizza.data
        pedidoPizza1.numPizza=pizzeria_form.numPizzas.data

        costoPizza = int(pizzeria_form.tamaPizza.data)
        # ingrePizza = int(pizzeria_form.ingredientesPizza.data)
        totalPizza = int(pizzeria_form.numPizzas.data)
        subtotalPizza = str( (costoPizza+10)*totalPizza )
        totalPizza = "0"

        pedidoPizza1.subtotal = subtotalPizza
        pedidoPizza1.total = totalPizza

        db.session.add(pedidoPizza1)
        db.session.commit()
        return redirect('pizzeria')
    return render_template("modificarPedido.html",form=pizzeria_form)

@app.route("/eliminarPedido", methods=["POST"])
def eliminarPedido():
    if request.method == 'POST':
        # Obtener los ID de los pedidos seleccionados desde el formulario
        ids_seleccionados = request.form.getlist('pedidos_seleccionados')
        for id_pedido in ids_seleccionados:
            pedido = PedidosPizza.query.get(id_pedido)
            if pedido:
                db.session.delete(pedido)
                db.session.commit()        
        return redirect('pizzeria')
    
@app.route("/terminarPedido", methods=["POST"])
def terminarPedido():
    if request.method == 'POST':
        global mismaVenta
        max_id = db.session.query(db.func.max(PedidosPizza.numeroVenta)).scalar()
        print("------------------------------ ID máximo: {}".format(max_id))
        suma_subtotal = db.session.query(db.func.sum(PedidosPizza.subtotal)).filter(PedidosPizza.numeroVenta == max_id).scalar()
        print("------------------------------ Suma de subtotal para idVenta {}: {}".format(max_id, suma_subtotal))
        mismaVenta = False
        #Obtiene el nombre del cliente
        nombreCliente = db.session.query(PedidosPizza.nombre).filter(PedidosPizza.numeroVenta == max_id).first()[0]

        #Ingresa una nueva venta
        nuevaVenta = VentasPizzas(
            nombre=nombreCliente,
            numeroVenta=max_id,
            total=suma_subtotal
        )
        db.session.add(nuevaVenta)
        db.session.commit()

        #Actualizar estatus ----------------------------------------------------------------------
        stmt = update(PedidosPizza).where(PedidosPizza.numeroVenta == max_id).values(estatus=0)
        db.session.execute(stmt)
        db.session.commit()
        mismaVenta = False

        return redirect('pizzeria')

@app.route("/pedidosFecha", methods=["POST"])
def pedidosFecha():
    formFecha = forms.ConsultaPedidosForm(request.form)
    pizzeria_form=forms.PizzeriaForm(request.form)
    fecha_seleccionada = formFecha.fecha_seleccionada.data

    if not fecha_seleccionada: 
        fecha_seleccionada = date.today()  
    ventasFecha = db.session.query(
    VentasPizzas.nombre,db.func.sum(VentasPizzas.total).label('total')).filter(VentasPizzas.create_date == fecha_seleccionada).group_by(VentasPizzas.nombre).all()
    return render_template("pizzeria.html",formF=formFecha, ventasFecha=ventasFecha, form=pizzeria_form)


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()

