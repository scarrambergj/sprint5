# Tipos de transaccion: RETIRO_EFECTIVO_CAJERO_AUTOMATICO:, 
# ALTA_TARJETA_CREDITO, 
# ALTA_CHEQUERA, 
# COMPRAR_DOLAR, 
# TRANSFERENCIA_ENVIADA, 
# TRANSFERENCIA_RECIBIDA
# Errores y excepciones a tener en cuenta: transacciones que dejen el monto en negativo y division por cero.


from packages.functions.functions import find_in_dict
from packages.JSON.schema import schema
from jsonschema import validate, ValidationError
import json
from os import path
from jinja2 import Environment, PackageLoader, select_autoescape
import sys

env = Environment(
    loader=PackageLoader("public"),
    autoescape=select_autoescape()
)

# template = env.get_template('template.html')

with open(sys.argv[1], 'r') as file:
    transacciones = json.load(file)
    try:
        validate(instance=transacciones, schema=schema)
    except ValidationError as error:
        print('El JSON esta mal formado')
        exit(1)

# print(template.render(transacciones=transacciones))

dir_especificaciones = path.join('packages', 'JSON', 'especificaciones.json')

with open(dir_especificaciones, 'r') as file:
    tipos_de_cuenta = json.load(file) 

specs_tipo = find_in_dict(transacciones, tipos_de_cuenta, 'tipo')

class Razon:
    def __init__(self, tipo, cupo_diario_restante, cantidad_extracciones, monto, saldo_cuenta, total_tc, total_c):
        self.tipo = tipo
        self.cupo_diario_restante = cupo_diario_restante
        self.cantidad_extracciones = cantidad_extracciones
        self.monto = monto
        self.saldo_cuenta = saldo_cuenta
        self.total_tc = total_tc
        self.total_c = total_c
        self.specs = specs_tipo
    
    def validar(self):
        if self.tipo == 'ALTA_CHEQUERA':
            self.alta_chequera()
        elif self.tipo == 'RETIRO_EFECTIVO_CAJERO_AUTOMATICO':
            self.retiro_efectivo()
        elif self.tipo == 'ALTA_TARJETA_CREDITO':
            self.alta_tarjeta()
        elif self.tipo == 'COMPRA_DOLAR':
            self.compra_dolar()
        elif self.tipo == 'TRANSFERENCIA_ENVIADA':
            self.transfer_env()
        elif self.tipo == 'TRANSFERENCIA_RECIBIDA':
            self.transfer_rec


    def alta_chequera(self):
        if self.total_c >= self.specs[7]:
            return f'Siendo de la clase {self.specs.clase.upper()} no podés acceder a más chequeras'
        else:
            raise Exception(f'La transaccion {self.tipo} ha sido rechazada pero no existe la suficiente informacion para validar por qué')

    def retiro_efectivo(self):
        if self.monto > self.cupo_diario_restante[6]:
            return f'El monto que estas intentando retirar es superior al cupo diario restante'

    def alta_tarjeta(self):
        pass

    def compra_dolar(self):
        pass

    def transfer_env(self):
        pass

    def transfer_rec(self):
        pass



class Cliente():
    def __init__(self, nombre, apellido, numero, dni, transacciones = []):
        self.nombre = nombre
        self.apellido = apellido
        self.numero = numero
        self.dni = dni
        self.transacciones = transacciones

    def agregar_transacciones(self, transacciones):
        for elem in transacciones.get('transacciones'):
            transaction = []
            if 'cantidadExtraccionesHechas' in elem.keys():
                elementoRemovido = elem.pop('cantidadExtraccionesHechas')
                for element in elem.values():
                    transaction.append(element)
                self.transacciones.append(Transacciones(*transaction, elementoRemovido))
            else:
                for element in elem.values():
                    transaction.append(element)
                self.transacciones.append(Transacciones(*transaction))
        self.tc_actual = self.transacciones[0].total_tc
        self.cheq_actual = self.transacciones[0].total_c

    def mostrar_razones(self):
        lista_razones = []
        for elem in self.transacciones:
            lista_razones.append(elem.razon.validar())
        return lista_razones
            
    def agregar_direccion(self, direc):
        self.direccion = direc

    def puede_crear_chequera(self):
        if self.cheq_actual < self.max_cheq:
            return 'Puede crear chequera'
        else:
            return 'No puede crear chequera'

    def puede_crear_tarjeta_credito(self):
        if self.tc_actual < self.max_tc:
            return 'Puede crear tarjeta de credito'
        else:
            return 'No puede crear tarjeta de credito'

    def puede_comprar_dolar(self):
        if self.dolar:
            return 'Puede comprar dolares'
        else:
            return 'No puede comprar dolares'

class Transacciones():
    def __init__(self, estado, tipo, cuenta_numero, cupo_diario_restante, monto, fecha, numero, saldo_cuenta, total_tc, total_c,  cantidad_extracciones=0):
        self.estado = estado
        self.tipo = tipo
        self.cuenta_numero = cuenta_numero
        self.cupo_diario_restante = cupo_diario_restante
        self.cantidad_extracciones = cantidad_extracciones
        self.monto = monto
        self.fecha = fecha
        self.numero = numero
        self.saldo_cuenta = saldo_cuenta
        self.total_tc = total_tc
        self.total_c = total_c
        if self.estado == 'RECHAZADA':
            self.razon = Razon(self.tipo, self.cupo_diario_restante, self.cantidad_extracciones, self.monto, self.saldo_cuenta, self.total_tc, self.total_c)
        else:
            self.razon = None

    def __str__(self) -> str:
        return f'{self.tipo} {self.cantidad_extracciones}'
    
class Tipo_Cuenta(Cliente):
    def __init__(self,nombre, apellido, numero, dni, tipo, transacciones=[]):
        super().__init__(nombre, apellido, numero, dni, transacciones=[])
        self.tipo = tipo
        self.dolar = self.tipo[3].get('caja_ahorro_usd')
        self.max_tc= self.tipo[5].get('max_tarjeta_credito')
        self.max_cheq = self.tipo[7].get('max_chequeras')

    def __str__(self) -> str:
        return f'{self.nombre} {self.apellido} {self.numero} {self.dni} {self.tipo} {self.direccion} {self.dolar} {self.transacciones}' 


class Direccion():
    def __init__(self, calle, numero, ciudad, provincia, pais):
        self.calle = calle
        self.numero = numero
        self.ciudad = ciudad
        self.provincia = provincia
        self.pais = pais

cuenta = Tipo_Cuenta(transacciones.get('nombre'), transacciones.get('apellido'), transacciones.get('numero'), transacciones.get('dni'), specs_tipo)
cuenta.agregar_direccion(transacciones.get('direccion'))
cuenta.agregar_transacciones(transacciones)
print(cuenta.puede_crear_tarjeta_credito())
print(cuenta.puede_crear_chequera())
print(cuenta.transacciones[1].razon.alta_chequera())