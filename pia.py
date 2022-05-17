from collections import namedtuple
import datetime
import sqlite3
from sqlite3 import Error
import sys


Equipos_s = namedtuple("Equipos_s","equipo s_descripcion e_descripcion cargo_e fecha_capturada Nombre_cliente")
diccionario_ventas={}
programa=1
parte_2 = 1
programa_abierto = 0

#esta primera parte es el menu y se desplaza con elif
while programa_abierto == 0:
    print ("menu")
    print("[1] registrar una venta ")
    print("[2] consultar una venta mediante el folio ")
    print("[3] consultar una venta mediante la fecha ")
    print("[4] consultar folio y cliente mediante fecha ")
    print("[5] salir")
    respuesta = int(input())
    #aqui esta la primera parte que es registrar
    if respuesta == 1:
        parte_2 = 1
        programa=1
        while programa==1:
            total_equipos =[]
            cargo_total=[]
            print(f"REGISTRO DE SERVICIO\n")
            Nombre_cliente = input("Nombre del cliente\n")
            while True:
                folio = int(input("escriba el folio de la venta (numero):"))
                if folio in diccionario_ventas.keys():
                    print('Error, ya existe una venta con ese folio de venta')
                else:
                    break
            while True:
                try:
                    fecha_capturada = input("escribe la fecha en este formato dd/mm/yyyy: ")
                    fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
                    break
                except Exception:
                    print("introdujo mal la fecha")
            #en esta parte lo dividimos porque un mismo folio tendria varios equipos
            while parte_2== 1:
                equipo = input("introduzca el nombre del equipo\n")
                s_descripcion = input("describa el servicio que se le realizara al equipo\n")
                e_descripcion = input("descripcion del estado actual del equipo\n")
                cargo_e = int(input("intoduzca el cargo de este servicio:"))

                Continuar = input("desea agregar un nuevo equipo? si/no\n")
            #aqui se agrega la tupla al diccionario y da el total
                if Continuar == "no":
                    cargo_total.append(cargo_e)
                    #aqui utilizamos la tupla para unir las cosas
                    equipo_info=Equipos_s(equipo, s_descripcion, e_descripcion, cargo_e, fecha_capturada,Nombre_cliente)
                    total_equipos.append(equipo_info)

                    diccionario_ventas[folio] = total_equipos
                    subtotal = sum(cargo_total)
                    total = subtotal * 1.16
                    print(f"el total a pagar es: ", total)
                    programa=0
                    parte_2=0
                elif Continuar == "si":
                    cargo_total.append(cargo_e)
                    #aqui utilizamos la tupla para unir las cosas
                    equipo_info=Equipos_s(equipo, s_descripcion, e_descripcion, cargo_e, fecha_capturada,Nombre_cliente)
                    total_equipos.append(equipo_info)
                    print("continue con el siguiente equipo: \n")
                else:
                    print("error no se guardo porque no se dio una opcion")
                    break

    elif respuesta==2:#aqui se consulta mediante el folio
        try:
            consulta = int(input('Folio a consultar: '))
            dimension = 0
            total_ventas = 0
            if consulta in diccionario_ventas.keys():
                while dimension < len(diccionario_ventas[consulta]):
                    print(f'nombre del equipo: {diccionario_ventas[consulta][dimension].equipo}')
                    print(f'Descripción del estado del equipo: {diccionario_ventas[consulta][dimension].e_descripcion}')
                    print('Precio: ${:.2f}'.format(diccionario_ventas[consulta][dimension].cargo_e, 2))
                    print(f'Fecha: {diccionario_ventas[consulta][dimension].fecha_capturada}')

                    total_ventas = (diccionario_ventas[consulta][dimension].cargo_e) + total_ventas
                    dimension += 1
                totalventa_iva = total_ventas *1.16
                print(f"el total del pedido fue \n$", totalventa_iva)
            else:
                print("no se encontro su consulta en el diccionario de las ventas")
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

    elif respuesta == 3: #aca se consulta metiante la fecha tuvimos bastantes problemas aqui pero diria que ya quedo
        try:
            while True:
                try:
                    fecha_busqueda = input("Ingrese la fecha para encontrar las ventas de ese día (ej: dd/mm/yyyy)\n» ")
                    fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
                    break
                except Exception:
                    print("introdujo mal la fecha")

            datomin = False
            total_ven_fecha = 0
            totalventa = 0


            for key, valor in diccionario_ventas.items() :
                contador_tupla = len(valor)
                contador = 0
                while contador < contador_tupla:
                    fechaExtraida = valor[contador].fecha_capturada

                    if fecha_busqueda == fechaExtraida:
                        print ("se encontro lo siguiente \n")
                        print(f'{key}  \n{valor[contador].equipo}  \n{valor[contador].s_descripcion}   \n{valor[contador].e_descripcion} \n${valor[contador].cargo_e} \n {valor[contador].fecha_capturada[-10:]}\n{valor[contador].Nombre_cliente}\n')
                        total_ven_fecha += valor[contador].cargo_e*1.16
                        contador+= 1
                    else:
                        print("no se encontro ninguna fecha")

                print(f"el total vendido es:{total_ven_fecha}")
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

    elif respuesta == 4:#consulta folio y cliente en base a fecha
        try:
            while True:
                try:
                    fecha_busqueda = input("Ingrese la fecha para encontrar las ventas de ese día (ej: dd/mm/yyyy)\n» ")
                    fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
                    break
                except Exception:
                    print("introdujo mal la fecha")

            datomin = False

            totalventa = 0


            for key, valor in diccionario_ventas.items() :
                contador_tupla = len(valor)
                contador = 0
                while contador < contador_tupla:
                    fechaExtraida = valor[contador].fecha_capturada

                    if fecha_busqueda == fechaExtraida:
                        print ("se encontro lo siguiente \n")
                        print(f'{key}  \n{valor[contador].Nombre_cliente}')

                        contador+= 1
                    else:
                        print("no se encontro ninguna fecha")

        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")


    elif respuesta == 5:#Creación de Base de datos y cierre del programa
        try:
            with sqlite3.connect("Ventasequipo.db") as conn: #se establece la conexion
                c = conn.cursor() #Creo cursor con instrucciones
                c.execute("CREATE TABLE IF NOT EXISTS Desc_ventas (descnum INTEGER PRIMARY KEY NOT NULL,cliente TEXT NOY NULL, servicio_descripcion TEXT NOT NULL,equipo_nombre TEXT NOT NULL,estado_descripcion TEXT NOT NULL, precio REAL NOT NULL,fecha TEXT NOT NULL, folio INTEGER NOT NULL);") #Envio instrucciones 
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()

        cantelem_folio = 0
        descnum = 0

        for key, valor in diccionario_ventas.items():
            cantelem_folio = len(valor)
            folio = key
            contador2 = 0
            fecha = valor[contador2].fecha_capturada
            contador2 += 1



            contador = 0
            while contador < cantelem_folio:

                descnum += 1
                cliente = valor[contador].Nombre_cliente
                servicio_descripcion = valor[contador].s_descripcion
                equipo_nombre = valor[contador].equipo
                estado_descripcion = valor[contador].e_descripcion
                precio = valor[contador].cargo_e
                fecha =valor[contador].fecha_capturada
                contador += 1 #para el while

                #Guardado en db
                try:
                    with sqlite3.connect("Ventasequipo.db") as conn: #1 Establezco conexion
                        c = conn.cursor() # Creo cursor con instrucciones
                        c.execute("INSERT INTO Desc_ventas VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (descnum,cliente,servicio_descripcion,equipo_nombre,estado_descripcion,precio,fecha,folio))
                except Error as e:
                    print(e)
                except Exception:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                finally:
                    if conn:
                        conn.close()
        print("el programa se ah cerrado")

        programa_abierto = 1

    else:#opcion por si te equivocaste
        print("respuesta invalida")

