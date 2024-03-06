from wtforms import Form
from wtforms import StringField,SelectField,RadioField,EmailField,IntegerField
from wtforms import validators


class EmpleadosForm(Form):
    id = IntegerField('id')
    nombre= StringField('nombre',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4,max=10,message='ingresa nombre valido')
    ])
    correo= EmailField('correo',[
        validators.Email(message='Ingresa un correo valido'),
    ])
    telefono= StringField('telefono',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4,max=10,message='Ingresa un telefono valido')
    ])
    direccion= StringField('direccion',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4,max=10,message='Ingresa una direccion valida')
    ])
    sueldo= StringField('sueldo',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4,max=10,message='Ingresa una sueldo valida')
    ])

class PizzeriaForm(Form):
    id = IntegerField('id')
    nombre= StringField('nombre',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4,max=10,message='ingresa nombre valido')
    ])
    direccion= StringField('direccion',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4,max=10,message='Ingresa una direccion valida')
    ])
    telefono= StringField('telefono',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4,max=10,message='Ingresa un telefono valido')
    ])
    numPizzas= IntegerField('Número Pizzas',[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=1,message='Ingresa una cantidad valida'),
    ])
    
    tamaPizza = RadioField('Tamaño Pizza', 
       choices=[
            ('1','Chica $40'),
            ('2','Mediana $80'),
            ('2','Grande $120')
            ], 
        validators=[validators.InputRequired()])
    ingredientesPizza = RadioField('Ingredientes Pizza', 
       choices=[
            ('1','Jamon $10'),
            ('2','Piña $10'),
            ('2','Champiñones $120')
            ], 
        validators=[validators.InputRequired()])
    subtotal= StringField('Subtotal')
    total= StringField('Total')

