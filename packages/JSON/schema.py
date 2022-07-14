transacciones = { 
                'estado' : { 'enum': ['ACEPTADA', 'RECHAZADA'] },
                'tipo' : { 'enum': ['RETIRO_EFECTIVO_CAJERO_AUTOMATICO', 'ALTA_TARJETA_CREDITO', 'ALTA_CHEQUERA', 'COMPRAR_DOLAR', 'TRANSFERENCIA_ENVIADA', 'TRANSFERENCIA_RECIBIDA'] },
                'cuentaNumero' : {'type': 'number'},
                'cupoDiarioRestante': {'type':'number'},
                'monto':{'type':'number'},
                'fecha':{'type': 'string'},
                'numero':{'type': 'number'},
                'saldoEnCuenta': {'type': 'number'},
                'totalTarjetasDeCreditoActualmente': {'type':'number'},
                'totalChequerasActualmente': {'type': 'number'}
                }

schema =  {
    'type': 'object',
    'properties': {
    'numero' : {'type' : 'number'},
    'nombre' : {'type' : 'string'},
    'apellido' : {'type' : 'string'},
    'dni' : {'type' : 'string'},
    'tipo' : {'enum' : ['CLASSIC', 'GOLD', 'BLACK']},
    'transacciones' : {
        'type': 'array',
        'items': {
          'type': 'object',
          'properties': transacciones,
          'additionalProperties': transacciones 
        },
    }
  }
}