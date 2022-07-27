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



with open(sys.argv[1], 'r') as file:
    transacciones = json.load(file)
    try:
        validate(instance=transacciones, schema=schema)
    except ValidationError as error:
        print('El JSON esta mal formado')
        exit(1)



dir_especificaciones = path.join('packages', 'JSON', 'especificaciones.json')

with open(dir_especificaciones, 'r') as file:
    tipos_de_cuenta = json.load(file) 

specs_tipo = find_in_dict(transacciones, tipos_de_cuenta, 'tipo')

class Razon:
    def __init__(self, estado, tipo, cupo_diario_restante, cantidad_extracciones, monto, saldo_cuenta, total_tc, total_c):
        self.estado = estado
        self.tipo = tipo
        self.cupo_diario_restante = cupo_diario_restante
        self.cantidad_extracciones = cantidad_extracciones
        self.monto = monto
        self.saldo_cuenta = saldo_cuenta
        self.total_tc = total_tc
        self.total_c = total_c
        self.specs = specs_tipo
    
    def alta_chequera(self):
        if self.total_c >= self.specs[7]['max_chequeras']:
            return f'Siendo de la clase {self.specs[0]["clase"].upper()} alcanzaste el maximo de chequeras'
        else:
            raise Exception(f'La transaccion {self.tipo} ha sido rechazada pero no existe la suficiente informacion para validar por qué')

    def retiro_efectivo(self):
        if self.monto > self.cupo_diario_restante:
            return f'El monto que estas intentando retirar es superior al cupo diario restante'
        elif self.monto > self.saldo_cuenta:
            return f'El monto que estas intentando retirar es superior al saldo restante en tu cuenta'
        # else:
        #     raise Exception(f'La transaccion {self.tipo} ha sido rechazada pero no existe la suficiente informacion para validar por qué')

    def alta_tarjeta(self):
        if self.total_tc >= self.specs[5]['max_tarjeta_credito']:
            return f'Siendo de la clase {self.specs[0]["clase"].upper()} alcanzaste el maximo de tarjetas de credito'
        else:
            raise Exception(f'La transaccion {self.tipo} ha sido rechazada pero no existe la suficiente informacion para validar por qué')

    def compra_dolar(self):
        if self.specs[3]['caja_ahorro_usd'] == False:
            return f'Siendo de la clase {self.specs[0]["clase"].upper()} no podés comprar dolares'
        elif self.monto > self.cupo_diario_restante or self.monto > self.saldo_cuenta:
            return f'El monto que estas intentando cambiar es superior al cupo diario restante'
        else:
            raise Exception(f'La transaccion {self.tipo} ha sido rechazada pero no existe la suficiente informacion para validar por qué')

    def transfer_env(self):
            monto_parcial = ((self.monto/100)*self.specs[8]['comision_transferencia'])
            monto_total = monto_parcial + self.monto
            if monto_total > self.saldo_cuenta:
                if monto_total == self.monto:
                    return f'El monto que estas intentando transferir es superior al saldo de tu cuenta'
                else:
                    return f'El monto que estas intentando transferir, aplicado el descuento por comisión, es superior al saldo de tu cuenta'
            elif monto_total >  self.specs[9]['monto_max_transferencia']:         
                if monto_total == self.monto:
                    return f'El monto que estas intentando transferir es superior al saldo de tu cuenta'
                else:
                    return f'El monto que estas intentando transferir, aplicado el descuento por comisión, es superior al saldo de tu cuenta'
    def transfer_rec(self):
        return 'La transferencia no fue autorizada'

    def validar(self):
        if self.estado == 'RECHAZADA':
            if self.tipo == 'ALTA_CHEQUERA':
                return self.alta_chequera()
            elif self.tipo == 'RETIRO_EFECTIVO_CAJERO_AUTOMATICO':
                return self.retiro_efectivo()
            elif self.tipo == 'ALTA_TARJETA_CREDITO':
                return self.alta_tarjeta()
            elif self.tipo == 'COMPRA_DOLAR':
                return self.compra_dolar()
            elif self.tipo == 'TRANSFERENCIA_ENVIADA':
                return self.transfer_env()
            elif self.tipo == 'TRANSFERENCIA_RECIBIDA':
                return self.transfer_rec()
        else:
            return ' '



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

    def mostrar_transacciones(self):
        trans = []
        for elem in self.transacciones:
            trans.append(elem.mostrar_transaccion())
        return trans

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

    def mostrar_cliente(self):
        return [self.nombre, self.apellido, self.numero, self.dni, self.direccion]

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
        self.razon = Razon(self.estado, self.tipo, self.cupo_diario_restante, self.cantidad_extracciones, self.monto, self.saldo_cuenta, self.total_tc, self.total_c)
        
            

    def __str__(self) -> str:
        return f'{self.fecha} {self.tipo} {self.estado} {self.monto}'

    def mostrar_transaccion(self):
        return [self.fecha, self.tipo, self.estado, self.monto]
    
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
    
    def __str__(self):
        return '{}{}{}{}{}'.format(self.calle, self.numero, self.ciudad, self.provincia, self.pais)

cuenta = Tipo_Cuenta(transacciones.get('nombre'), transacciones.get('apellido'), transacciones.get('numero'), transacciones.get('dni'), specs_tipo)
cuenta.agregar_direccion(list(transacciones.get('direccion').values()))
cuenta.agregar_transacciones(transacciones)

lista_razones = cuenta.mostrar_razones()
lista_transacciones = cuenta.mostrar_transacciones()
info_cliente = cuenta.mostrar_cliente()

env = Environment(
    loader=PackageLoader("public"),
    autoescape=select_autoescape()
)

template = env.get_template('template.html')
archivo = template.render(razones=lista_razones, transacciones=lista_transacciones, cliente=info_cliente).encode('UTF-8')

with open('reporte.html', 'wb') as file:
    file.write(archivo)
