"""
Se incluyen funciones para convertir a letra cantidades positivas menores que un millón.
"""

unidades = (
    'cero',
    'un',
    'dos',
    'tres',
    'cuatro',
    'cinco',
    'seis',
    'siete',
    'ocho',
    'nueve'
)

dieci = (
    'diez',
    'once',
    'doce',
    'trece',
    'catorce',
    'quince',
    'dieciséis',
    'diecisiete',
    'dieciocho',
    'diecinueve'
)

veinti = (
    'veinte',
    'veintiún',
    'veintidós',
    'veintitrés',
    'veinticuatro',
    'veinticinco',
    'veintiséis',
    'veintisiete',
    'veintiocho',
    'veintinueve'
)

decenas = (
    'cero',
    'diez',
    'veinte',
    'treinta',
    'cuarenta',
    'cincuenta',
    'sesenta',
    'setenta',
    'ochenta',
    'noventa'
)

centenas = (
    'cero',
    'ciento',
    'doscientos',
    'trescientos',
    'cuatrocientos',
    'quinientos',
    'seiscientos',
    'setecientos',
    'ochocientos',
    'novecientos'
)

def leer_unidades(cantidad):
    assert(cantidad > 0 and cantidad < 10)
    return unidades[cantidad]
    
def leer_decenas(cantidad):
    assert(cantidad >= 10 and cantidad < 100)
    decena, unidad = divmod(cantidad, 10)
    if decena > 2 and unidad != 0:
        return (' y '.join([decenas[decena], leer_unidades(unidad)]))
    elif decena > 2 and unidad == 0:
        return decenas[decena]
    elif decena == 2:
        return veinti[unidad]
    else:
        return dieci[unidad]

def leer_centenas(cantidad):
    assert(cantidad >= 100 and cantidad < 1000)

    centena, residuo = divmod(cantidad, 100)
    if centena == 1 and residuo == 0:
        return 'cien'
    else:
        return (' '.join([centenas[centena], half_cantidad_letra(residuo)]))

def half_cantidad_letra(cantidad):
    if cantidad == 0:
        return ''
    if cantidad > 0 and cantidad < 10:
        return leer_unidades(cantidad)
    elif cantidad >= 10 and cantidad < 100:
        return leer_decenas(cantidad)
    elif cantidad >= 100 and cantidad < 1000:
        return leer_centenas(cantidad)

def cantidad_letra(cantidad):
    assert(cantidad < 1000000)

    if cantidad == 0:
        return 'cero'

    centenas_millar, residuo = divmod(cantidad, 1000)
    if centenas_millar:
        return (half_cantidad_letra(centenas_millar) + ' mil ' + half_cantidad_letra(residuo)) 
    else:
        return half_cantidad_letra(residuo)

def cantidad_letra_from_float(float_cantidad):
    cantidad = int(float_cantidad)
    return cantidad_letra(cantidad), str(float_cantidad).split('.')[1].ljust(2, '0') if len(str(float_cantidad).split('.')[1]) < 2 else str(float_cantidad).split('.')[1]
