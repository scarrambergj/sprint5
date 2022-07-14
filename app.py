# Tipos de transaccion: RETIRO_EFECTIVO_CAJERO_AUTOMATICO:, 
# ALTA_TARJETA_CREDITO, 
# ALTA_CHEQUERA, 
# COMPRAR_DOLAR, 
# TRANSFERENCIA_ENVIADA, 
# TRANSFERENCIA_RECIBIDA
# Errores y excepciones a tener en cuenta: transacciones que dejen el monto en negativo y division por cero.

from packages.JSON.schema import schema
from jsonschema import validate, ValidationError
import json

with open('pruebaJSON.json', 'r') as file:
    transacciones = json.load(file)
    try:
        validate(instance=transacciones, schema=schema)
    except ValidationError as error:
        print('El JSON esta mal formado')


class Cliente():
    def __init__(self, nombre, apellido, numero, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.numero = numero
        self.dni = dni

    def puede_crear_chequera(self):
        pass
    # Debe retornar un booleano

    def puede_crear_tarjeta_credito(self):
        pass
    # Debe retornar un booleano

    def puede_comprar_dolar(self):
        pass
    # Debe retornar un booleano
