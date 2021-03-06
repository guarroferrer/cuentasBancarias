__author__ = 'jordiblanchsalgado'

#-*_ coding: UTF-8 _*_

from persona import Persona
from cuenta import Cuenta
from empresa import Empresa
from movimientos import Movimientos
import datetime
from random import randrange




print("")
print("-----> BIENVENIDO AL GEORGE NATIONAL BANK <-----")
def menu():
    print("")
    print("¿Que desea hacer ahora?")
    print(" 0-.¡Añadir una cuenta!  (RECUERDE QUE NECESITARA UNA CUENTA ANTES DE USAR LAS OTRAS OPCIONES) ")
    print(" 1-.Consultar saldo ")
    print(" 2-.Realizar un movimiento (ingresar/retirar)")
    print(" 3-.Listar mis movimientos")
    print(" 4-.Salir")
def menuMovi():
    print("¿Que desea hacer en la cuenta ?")
    print("1-. Ingresar")
    print("2-. Retirar")
    print("3-. Atras")

eleccion = 0
eleccionMovi = 0
varNombre = ""
menu()
while eleccion != 4:
    eleccion = int(input())

    #AÑADIR CUENTA
    if eleccion == 0:
        print("1-. Cuenta de un particular")
        print("2-. Cuenta de una empresa")
        tipo = int(input())
        #PARTICULAR
        if tipo == 1:
            nombre = ""
            apellido1 = ""
            apellido2 = ""
            print("nombre y apellidos(ej: Jordi Blanch Salgado):")
            nombreCompleto = str(input())
            var = nombreCompleto.split()
            nombre = var[0]
            apellido1 = var[1]
            apellido2 = var[2]
            print("Dni/Nif:")
            dni = str(input())

            #CREACION PERSONA
            persona = Persona(nombre,apellido1,apellido2,dni)
            nombrePersona = persona.getNombreCompleto()
            nif = persona.getNif()

            #ESCRIBIR EL TITULARES.TXT
            with open('titulares.txt', mode='a', encoding='utf-8')as archivo:
                archivo.write(nombrePersona+","+nif+"\n")

            #CREACION CUENTA
            print("\nCreación de cuenta para particular:")
            iban = str(randrange(2000,2999))
            iban += " "+str(randrange(0,9999)).zfill(4)
            iban += " "+str(randrange(0, 99)).zfill(2)
            iban += " "+str(randrange(1000000000, 9999999999))

            print("Introduce la moneda ")
            moneda = str(input())
            saldo = "0"

            #ESCRIBIR CUENTA
            with open('cuentas.txt',mode='a', encoding='utf-8')as archivo:
                archivo.write(nombrePersona+","+iban+","+moneda+","+saldo+"\n")
            menu()
        #EMPRESA
        if tipo == 2:
            print("Razón social:")
            varNombre = str(input())
            print("Cif:")
            varCif = str(input())

            #CREACION EMPRESA
            empresa = Empresa(varNombre,varCif)
            nombreEmpresa = empresa.getNombre()
            cif = empresa.getCif()
            print(nombreEmpresa,cif)

            #ESCRIBIR EL TITULARES.TXT
            with open('titulares.txt', mode='a', encoding='utf-8')as archivo:
                archivo.write(nombreEmpresa+","+cif+"\n")

            #CREACION CUENTA
            print("\nCreación de cuenta para empresa:")
            iban = str(randrange(2000,2999))
            iban += " "+str(randrange(0,9999)).zfill(4)
            iban += " "+str(randrange(0, 99)).zfill(2)
            iban += " "+str(randrange(1000000000, 9999999999))
            print("Introduce la moneda ")
            moneda = str(input())
            saldo = "0"

            #ESCRIBIR CUENTA
            with open('cuentas.txt',mode='a', encoding='utf-8')as archivo:
                archivo.write(nombreEmpresa+","+iban+","+moneda+","+saldo+"\n")
            menu()


    #CONSULTAR SALDO
    if eleccion == 1:
        print("Introduce el nombre completo del titular,ya se un particular o una empresa (ej: Jordi Blanch Salgado)")
        varTitularN = str(input())
        encontrado = False
        try:
            with open('cuentas.txt',mode='r',encoding='utf-8')as archivo:
                for linia in archivo:
                    titularN, iban, moneda, saldo= linia.split(',',3)
                    varSaldo = saldo.strip("\n")


                    if  titularN.upper() == varTitularN.upper():
                        print(varSaldo,moneda)
                        encontrado = True
                        menu()

                if encontrado == False:
                    print("No encontrado este titular en la base de datos")
                    menu()
        except:
            print("No existe el archivo cuentas.txt , primero debe crear una cuenta!")
            menu()



    #MOVIMIENTOS
    if eleccion == 2:
        print("Debemos identificar la cuenta:")
        print("Introduce tu nombre completo (ej: Jordi Blanch Salgado):")
        nombre = str(input())
        encontrado = False
        eleccionMovi = 0

        with open('cuentas.txt',mode='r',encoding='utf-8')as archivo:
            for linia in archivo:
                try:
                    titular,iban,moneda,saldo= linia.split(',', 3)
                    saldo = saldo.strip("\n")
                except:
                    print("")

                if nombre.upper() == titular.upper():
                    cuenta = Cuenta(iban,titular,moneda)
                    encontrado = True

                    varIban = cuenta.getIban()
                    varMoneda = cuenta.getMoneda()
                    varSaldo = saldo

                    while eleccionMovi != 3:
                        menuMovi()
                        eleccionMovi = int(input())

                        #INGRESAR
                        if eleccionMovi == 1:
                            print("Introduzca la cantidad a ingresar:")
                            importe = int(input())
                            signo = "+"
                            i = datetime.datetime.now()
                            now= str(i.day)+"/"+str(i.month)+"/"+str(i.year)+" "+str(i.hour)+":"+ str(i.minute)+":"+str(i.second)

                            movimiento = Movimientos(now,varIban,importe,signo)

                            fecha = movimiento.getFecha()
                            iban = movimiento.getIban()
                            importe = movimiento.getImporte()
                            signo = movimiento.getSigno()

                            with open('cuentas.txt',mode='r',encoding='utf-8')as archivo:
                                contenido = ""
                                contModificad = ""
                                for linia in archivo:
                                    titular,iban,moneda,saldo = linia.split(',',3)
                                    saldo = saldo.strip("\n")

                                    nuevoTit = titular.upper()
                                    nuevoNom = nombre.upper()

                                    if nuevoNom != nuevoTit:
                                        contenido = contenido + (nuevoTit+","+iban+","+moneda+","+saldo+"\n")

                                    else:
                                        varSaldo = int(saldo)
                                        saldoAct = varSaldo + importe
                                        contModificad = titular+","+iban+","+moneda+","+str(saldoAct)+"\n"

                                contTotal = contenido+contModificad

                            with open('cuentas.txt',mode='w',encoding='utf-8')as archivo:
                                archivo.write(contTotal)
                                print("")
                                print("---INGRESADO---")
                                print("")

                            #UPDATE FICHERO MOVIMIENTOS
                            contMovi = str(fecha)+","+str(iban)+","+signo+""+str(importe)+"\n"
                            with open('movimientos.txt',mode='a',encoding='utf-8')as archivo:
                                archivo.write(contMovi)
                        #RETIRAR
                        if eleccionMovi == 2:
                            print("Introduzca la cantidad a retirar:")
                            importe = int(input())
                            signo = "-"
                            i = datetime.datetime.now()
                            now= str(i.day)+"/"+str(i.month)+"/"+str(i.year)+" "+str(i.hour)+":"+ str(i.minute)+":"+str(i.second)

                            movimiento = Movimientos(now,varIban,importe,signo)

                            fecha = movimiento.getFecha()
                            iban = movimiento.getIban()
                            importe = movimiento.getImporte()
                            signo = movimiento.getSigno()

                            with open('cuentas.txt',mode='r',encoding='utf-8')as archivo:
                                contenido = ""
                                flag = False
                                for linia in archivo:
                                    titular,iban,moneda,saldo = linia.split(',',3)
                                    saldo = saldo.strip("\n")

                                    nuevoTit = titular.upper()
                                    nuevoNom = nombre.upper()

                                    if nuevoNom == nuevoTit:
                                        if int(saldo) > int(importe):
                                            saldoAct = int(saldo) - int(importe)
                                            contModificad = titular+","+iban+","+moneda+","+str(saldoAct)+"\n"

                                        else:
                                            flag = True
                                            print("")
                                            print("Saldo insuficiente")
                                            print("")
                                    else:
                                        contenido = contenido + (nuevoTit+","+iban+","+moneda+","+saldo+"\n")
                                contTotal = contenido+contModificad
                            if flag != True:
                                with open('cuentas.txt',mode='w',encoding='utf-8')as archivo:
                                    archivo.write(contTotal)
                                    print("")
                                    print("---RETIRADO---")
                                    print("")

                                #UPDATE FICHERO MOVIMIENTOS
                                contMovi = str(fecha)+","+str(iban)+","+signo+""+str(importe)+"\n"
                                with open('movimientos.txt',mode='a',encoding='utf-8')as archivo:
                                    archivo.write(contMovi)


                        if eleccionMovi == 3:
                            menu()
        if encontrado == False:
            print("Titular no encontrado")
            menu()


    if eleccion == 3:
        print("Debemos identificar la cuenta:")
        print("Introduce tu nombre completo (ej: Jordi Blanch Salgado):")
        nombre = str(input())

        with open('cuentas.txt',mode='r',encoding='utf-8')as archivo:
            encontrado = False
            for linia in archivo:
                titular,iban,moneda,saldo = linia.split(',',3)
                saldo = saldo.strip("\n")

                if titular.upper() == nombre.upper():
                    encontrado = True
                    varCuentaIban = iban
                    with open('movimientos.txt',mode='r',encoding='utf-8')as archivo:
                        for linia in archivo:
                            fecha,iban,movimiento = linia.split(',',2)
                            movimiento = movimiento.strip("\n")

                            if varCuentaIban == iban:
                                print(linia)

            if encontrado == False:
                print("Titular no encontrado")

        menu()

    if eleccion == 4:
        print("")
        print("Hasta la próxima")
        print("CERRANDO...")
    #SALIR
    if eleccion != 1 and eleccion != 2 and eleccion != 0 and eleccion != 3 and eleccion !=4:
        print("Introduce una opcion válida")

