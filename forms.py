from wtforms import Form
from wtforms import StringField,SelectField,RadioField,EmailField,IntegerField,DateField
from wtforms import validators
from wtforms.validators import DataRequired


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
        validators.DataRequired(message='el campo es requerido')
    ])
    direccion= StringField('direccion',[
        validators.DataRequired(message='el campo es requerido')
    ])
    telefono= StringField('telefono',[
        validators.DataRequired(message='el campo es requerido')
    ])
    numPizzas = IntegerField('Número Pizzas', [
        validators.DataRequired(message='El campo es requerido'),
        validators.NumberRange(min=1, message='El número de pizzas no puede ser negativo')
    ])
    
    tamaPizza = RadioField('Tamaño Pizza', 
       choices=[
            ('40','Chica $40'),
            ('80','Mediana $80'),
            ('120','Grande $120')
            ])
    ingredientesPizza = RadioField('Ingredientes Pizza', 
       choices=[
            ('1','Jamon $10'),
            ('2','Piña $10'),
            ('3','Champiñones $10')
            ])
    numVenta = StringField('numVenta')
    estatus= StringField('Estatus')
    subtotal= StringField('Subtotal')
    total= StringField('Total')

class ConsultaPedidosForm(Form):
    fecha_seleccionada = DateField('Seleccione una fecha', validators=[DataRequired()], format='%Y-%m-%d')