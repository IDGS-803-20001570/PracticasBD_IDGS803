from flask_sqlalchemy import SQLAlchemy

import datetime

db=SQLAlchemy()


class Empleados(db.Model):
    _tablename_='empleados'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    correo=db.Column(db.String(50))
    telefono=db.Column(db.String(50))
    direccion=db.Column(db.String(50))    
    sueldo=db.Column(db.String(50))
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)

class PedidosPizza(db.Model):
    _tablename_='pedidosPizza'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    direccion=db.Column(db.String(50))  
    telefono=db.Column(db.String(50))  
    tamaPizza=db.Column(db.String(50))
    ingredientesPizza=db.Column(db.String(50))
    numPizza=db.Column(db.String(50))
    subtotal=db.Column(db.String(50))    
    total=db.Column(db.String(50))
    numeroVenta=db.Column(db.String(50))  
    estatus=db.Column(db.String(50)) 
    fecha= db.Column(db.Date) 

class VentasPizzas(db.Model):
    tablename='ventas_pizza'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    numeroVenta=db.Column(db.String(50))  
    total=db.Column(db.String(50))
    create_date = db.Column(db.Date)