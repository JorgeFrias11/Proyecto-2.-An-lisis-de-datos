import csv 

# Lista para guardar el contenido del archivo csv
lista = []

with open("synergy_logistics_database.csv", "r", encoding = 'utf-8-sig') as archivo: 
    lector = csv.DictReader(archivo)
    
    for linea in lector: 
        lista.append(linea)

### DEFINICION DE FUNCIONES

# OPCION 1: GENERAR RUTAS
def gen_rutas(direccion): 

    contador = 0
    rutas_contadas = []
    conteo_rutas = []
    valores = []
    
      
    for ruta in lista: 
        ruta_actual = [ruta['origin'], ruta['destination']]
        if ruta['direction'] == direccion and ruta_actual not in rutas_contadas: 
            for movimiento in lista:
                if movimiento['direction'] == direccion:
                    if ruta_actual == [movimiento['origin'], movimiento['destination']]:
                        contador += 1
                        valores.append(int(movimiento['total_value']))
            rutas_contadas.append(ruta_actual)
            conteo_rutas.append([ruta['origin'], ruta['destination'], 
                                 contador, sum(valores)])
            contador = 0 
            del valores[:]
    
    conteo_rutas.sort(reverse = True, key = lambda x: x[3])
    
    ## Sacar total de movimientos y su valor 
    total_movimientos = 0
    total_valor = 0 
    for pais in conteo_rutas: 
        total_movimientos += pais[2]
        total_valor += pais[3]
    
    mejores_diez = conteo_rutas[0:10]
    
    ## Sacar total de movimientos y su valor para los 10 mejores
    movimientos_diez = 0
    valor_diez = 0
    for pais in mejores_diez: 
        movimientos_diez += pais[2]
        valor_diez += pais[3]

    return mejores_diez, total_movimientos, total_valor, movimientos_diez, valor_diez

# OPCION 1: MENSAJE A IMPRIMIR
def imprimir_rutas(direccion = 'Imports'):
    
    lista_rutas = gen_rutas(direccion)
    transaccion = []
    if direccion == 'Imports':
        transaccion = ['importación', 'Importaciones']
    else: 
        transaccion = ['exportación', 'Exportaciones']
    
    print(f'\nLas 10 rutas de {transaccion[0]} con más flujos son:')
    for ruta in lista_rutas: 
        print(f'\n\t{lista_rutas.index(ruta) + 1}. Ruta {ruta[0]} -> {ruta[1]}:'
              f'\n\t\tFlujos: ${ruta[3]:,}.'
              f'\n\t\t{transaccion[1]}: {ruta[2]}.'
              )

# OPCION 2: GENERAR TRANSPORTES
def gen_transportes(direccion = 'Imports'):
   
    contador = 0
    medios_contados = []
    conteo_medios = []
    valores = []
    
    for medio in lista: 
        medio_actual = medio['transport_mode']
        if medio['direction'] == direccion and medio_actual not in medios_contados: 
            for transporte in lista: 
                if transporte['direction'] == direccion:
                    if medio_actual == transporte['transport_mode']:
                        contador += 1
                        valores.append(int(transporte['total_value']))
            medios_contados.append(medio_actual)
            conteo_medios.append([medio['transport_mode'], contador, sum(valores)])
            contador = 0
            del valores[:]
    
    conteo_medios.sort(reverse = True, key = lambda x: x[2])

    return conteo_medios

## OPCION DOS: MENSAJE A IMPRIMIR
def imprimir_transportes(direccion = 'Imports'):
    
    lista_transportes = gen_transportes(direccion)
    transaccion = []
    if direccion == 'Imports':
        transaccion = ['importación', 'Importaciones']
    else: 
        transaccion = ['exportación', 'Exportaciones']
    
    print(f'\nLos medios de transporte más importantes para {transaccion[0]} son:')
    for medio in lista_transportes: 
        print(f'\n\t{lista_transportes.index(medio) + 1}. {medio[0]}:'
              f'\n\t\tValor total: ${medio[2]:,}.'
              f'\n\t\t{transaccion[1]}: {medio[1]:,}.'
              )

# OPCION 3: VALOR TOTAL IMPORTACIONES Y EXPORTACIONES
def gen_porcentajes(direccion = 'Imports'):

    contador = 0
    paises_contados = []
    conteo_paises = []
    valores = []
    valores_total = []
    eleccion = ''
      
    for pais in lista: 
        # Si se importa se considera el destino, sino el origen
        # Condicion para filtrar por destino u origen
        if direccion == 'Imports':
            eleccion = 'destination'
        else: 
            eleccion = 'origin'
           
        # Si se importa se considera el destino
        pais_actual = pais[eleccion]
        if pais['direction'] == direccion: 
            valores_total.append(int(pais['total_value']))
            if pais_actual not in paises_contados:
                for venta in lista:
                    if venta['direction'] == direccion and pais_actual == venta[eleccion]:
                        contador += 1
                        valores.append(int(venta['total_value']))
                                
                paises_contados.append(pais_actual)
                
                pais_total = sum(valores)
                conteo_paises.append([pais[eleccion], contador, pais_total])
                contador = 0 
                del valores[:]
    # Sacar suma total y el porcentaje correspondiente a cada país
    total = sum(valores_total)
    for pais in conteo_paises:
        porcentaje = round((pais[2]/total)*100, 2)
        pais.append(porcentaje)
    
    ## Ordenar por pocentaje de mayor a menor
    conteo_paises.sort(reverse = True, key = lambda x: x[2])    
    
    ## Contar los porcentajes hasta llegar al 80% del total 
    paises_importantes = []
    paises_no_importantes = []
    conteo_porcentajes = []
    for pais in conteo_paises:
        # Lista 1: paises que ocupan el 80%
        if sum(conteo_porcentajes) < 80:
            conteo_porcentajes.append(pais[3])
            paises_importantes.append(pais)
        # Lista 2: paises que ocupan el ultimo 20%
        else:
            paises_no_importantes.append(pais)
        
    return paises_importantes, paises_no_importantes

## OPCION 3: IMPRIMIR MENSAJE
def imprimir_porcentajes(direccion = 'Imports'):
    
    paises_importantes = gen_porcentajes(direccion)[0]
    paises_no_importantes = gen_porcentajes(direccion)[1]
    transaccion = ''
    if direccion == 'Imports':
        transaccion = 'importaciones'
    else: 
        transaccion = 'exportaciones'
    
    print(f'\nLos países que generan el 80% del valor de las {transaccion} son:')
    for pais in paises_importantes: 
        print(f'\n\t{paises_importantes.index(pais) + 1}. {pais[0]} - {pais[3]}%:'
              f'\n\t\tValor: ${pais[2]:,}.'
              f'\n\t\t{transaccion.title()}: {pais[1]:,}.'
              )
    
    print('\nEl resto de los países que generan el 20% faltante son:')
    for pais in paises_no_importantes: 
        print(f'\n\t{paises_no_importantes.index(pais) + 1}. {pais[0]} - {pais[3]}%:'
              f'\n\t\t{transaccion.title()}: {pais[1]:,}.'
              f'\n\t\tValor: ${pais[2]:,}.')     

# Mensaje de bienvenida
print('¡Bienvenido! :D')

# Variable para continuar o no viendo opciones
no_continua = 0
while no_continua != 1: 

    # Mensaje de Bienvenida y lista de opciones 
    print('\n¿Qué le gustaría ver?  ( ͡° ͜ʖ ͡°)')
    print('Lista de opciones:'
          '\n\ta. Rutas de importación y exportación.'
          '\n\tb. Medios de transporte.'
          '\n\tc. Valor total de importaciones y exportaciones.'
          )
    
    # Input para escoger una opcion de la lista 
    opcion = input('Elija una opción (a,b,c): ')
    
    # Variable y While para comprobar que se escoja una opción válida 
    opcion_valida = 0 
    
    while opcion_valida != 1: 
        
        ### Primer opcion
        if opcion == 'a':
            # opcion_valida cambia a 1 para romper el while
            opcion_valida = 1
            # Se muestran las subopciones
            print('\nEscogió "Rutas de importación y exportación".'
                  '\nSubopciones:'
                  '\n\ta. Por monto de importaciones.'
                  '\n\tb. Por monto de exportaciones.')
    
            subopcion = input('Elige una subopción (a,b): ')
            
            # Variable y while para comprobar que se escoja una opción válida
            subopcion_valida = 0
            
            while subopcion_valida != 1:
                
                # Subopción 1. subopcion_valida cambia a 1
                if subopcion == 'a':
                    subopcion_valida = 1
                    # Se llama a la funcion gen_rutas para Imports
                    imprimir_rutas('Imports')
                
                # Subopción 2. subopcion_valida cambia a 1
                elif subopcion == 'b': 
                    subopcion_valida = 1               
                    # Se llama a la funcion gen_rutas para Exports
                    imprimir_rutas('Exports')
                    
                else: 
                    print('Subopción inválida.')
                    subopcion = input('Intente otra vez (a,b): ')
        
        ### Segunda opcion
        elif opcion == 'b': 
            opcion_valida = 1
            print('\nEscogió "Medios de transporte."'
                  '\nSubopciones:'
                  '\n\ta. Por importaciones.'
                  '\n\tb. Por exportaciones.'
                  )
            
            subopcion = input('Elige una subopción (a,b): ')
            
            # Variable y while para comprobar que se escoja una opción válida
            subopcion_valida = 0
            
            while subopcion_valida != 1:
                
                # Subopción a. subopcion_valida cambia a 1
                if subopcion == 'a':
                    subopcion_valida = 1                
                    # Se llama a la funcion para imprimir el mensaje
                    imprimir_transportes('Imports')
                        
                # Subopción b. subopcion_valida cambia a 1
                elif subopcion == 'b':
                    subopcion_valida = 1
                    # Se llama a la funcion para imprimir el mensaje
                    imprimir_transportes('Exports')
                    
                else: 
                    print('Subopción inválida.')
                    subopcion = input('Intente otra vez (a,b): ')
        
        ### Tercera opcion
        elif opcion == 'c':
            opcion_valida = 1
            
            print('\nEscogió "Valor total de importaciones y exportaciones."'
                  '\nSubopciones:'
                  '\n\ta. Por importaciones.'
                  '\n\tb. Por exportaciones.'
                  )
            
            subopcion = input('Elige una subopción (a,b): ')
            
            # Variable y while para comprobar que se escoja una opción válida
            subopcion_valida = 0
            
            while subopcion_valida != 1:
                
                 # Subopción a. subopcion_valida cambia a 1
                if subopcion == 'a':
                    subopcion_valida = 1               
                    # Se llama a la funcion para imprimir el mensaje
                    imprimir_porcentajes('Imports')
                        
                # Subopción b. subopcion_valida cambia a 1
                elif subopcion == 'b':
                    subopcion_valida = 1    
                    # Se llama a la funcion para imprimir el mensaje
                    imprimir_porcentajes('Exports')              
                    
                else: 
                    print('Subopción inválida.')
                    subopcion = input('Intente otra vez (a,b): ')
        
        ## Repetir el input si s ingresó una opción no valida
        else: 
            print('Opción inválida.')
            opcion = input('Intente otra vez: ')
    
    ## Controlar si el usuario verá otra opción o no    
    continuar = input('\n¿Desea ver algo más? (si/no) ' )    
    if continuar == 'si': 
      continue
    elif continuar == 'no':
      print('¡Hasta pronto!')
      no_continua = 1
    else: 
      print('Opción invalida. Intente otra vez.')
      continuar = input('¿Desea ver algo más? (si/no)')
      

