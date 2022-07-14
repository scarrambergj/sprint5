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
    def __init__(self, nombre, apellido, numero, dni, transacciones = []):
        self.nombre = nombre
        self.apellido = apellido
        self.numero = numero
        self.dni = dni

    def agregar_transaccion(self, transaccion):
        self.transacciones.append(transacciones)

    def agregar_direccion(direc):
        __direccion = direc

    def puede_crear_chequera(self, cheq_actual, max_cheq):
        return cheq_actual < max_cheq

    def puede_crear_tarjeta_credito(self, tc_actual, max_tc):
        return tc_actual < max_tc

    def puede_comprar_dolar(self, dolar):
        return dolar

class Transaccion():
    def __init__(self, estado, razon, cuenta_numero, cupo_diario_restante, cantidad_extracciones, monto, fecha, numero, saldo_cuenta, total_tc, total_c):
        self.tipo = estado
        self.razon = razon
        self.cuenta_numero = cuenta_numero
        self.cupo_diario_restante = cupo_diario_restante
        self.cantidad_extracciones = cantidad_extracciones
        self.monto = monto
        self.fecha = fecha
        self.numero = numero
        self.saldo_cuenta = saldo_cuenta
        self.total_tc = total_tc
        self.total_tc = total_c
    
class Razon:
    def __init__(self, tipo):
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

