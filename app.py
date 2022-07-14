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

with open('pruebaJSON.json', 'r') as file:
    transacciones = json.load(file)
    try:
        validate(instance=transacciones, schema=schema)
    except ValidationError as error:
        print('El JSON esta mal formado')

dir_especificaciones = path.join('packages', 'JSON', 'especificaciones.json')


with open(dir_especificaciones, 'r') as file:
    tipos_de_cuenta = json.load(file) 

specs_tipo = find_in_dict(transacciones, tipos_de_cuenta, 'tipo')

class Cliente():
    def __init__(self, nombre, apellido, numero, dni, cuentas = []):
        self.nombre = nombre
        self.apellido = apellido
        self.numero = numero
        self.dni = dni

    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)

    def agregar_direccion(direc):
        __direccion = direc

    def puede_crear_chequera(self):
        pass
    # Debe retornar un booleano

    def puede_crear_tarjeta_credito(self):
        pass
    # Debe retornar un booleano

    def puede_comprar_dolar(self):
        pass
    # Debe retornar un booleano

class Cuenta():
    def __init__(self):
        pass

class Tipo_Cuenta(Cliente):
    def __init__(self,nombre, apellido, numero, dni, tipo, cuentas=[]):
        self.tipo = tipo
        super().__init__(nombre, apellido, numero, dni, cuentas=[])


class Direccion():
    def __init__(self, calle, numero, ciudad, provincia, pais):
        self.calle = calle
        self.numero = numero
        self.ciudad = ciudad
        self.provincia = provincia
        self.pais = pais

