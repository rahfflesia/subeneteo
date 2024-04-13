import math
import tkinter as tk
from tkinter import ttk
# Funciones
# Esta función determina la clase según el rango
def claseIp(ip):
    if ip >= 0 and ip <= 127:
        return "A"
    elif ip >= 128 and ip <= 191:
        return "B"
    elif ip >= 192 and ip <= 223:
        return "C"
    else:
        return "Ese rango no corresponde a ninguna clase"

# Determina el número máximo de direcciones que puede manejar cada clase
def hostsMaximos(clase):
    if clase == "C":
        return 256
    elif clase == "B":
        return 65536
    elif clase == "A":
        return 16777216
    else:
        return 0

# Asigna los octetos correspondientes según la clase, si es C asigna 1 byte, si es B 2 bytes, si es A asigna 3 bytes
def obtenerOcteto(clase):
    if clase == "C":
        return 1
    elif clase == "B":
        return 2
    elif clase == "A":
        return 3
    else:
        return 0


def obtenerMascara(clase):
    if clase == "C":
        return "255.255.255.0"
    elif clase == "B":
        return "255.255.0.0"
    elif clase == "A":
        return "255.0.0.0"
    else:
        return "Máscara no definida"

def bitsDisponibles(octeto):
    if clase == "C":
        return octeto * 8
    elif clase == "B":
        return octeto * 8
    elif clase == "A":
        return octeto * 8


# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Calculadora de subredes")
etiquetaIp = ttk.Label(ventana, text="Ingresa la dirección ip")
etiquetaIp.pack()
direccion = tk.StringVar()
inputIp = ttk.Entry(ventana, textvariable=direccion)
inputIp.pack()
etiquetaSel = ttk.Label(ventana, text="Selecciona una opción")
etiquetaSel.pack()
opcionComboBox = tk.StringVar()
listaOpciones = ttk.Combobox(ventana, textvariable=opcionComboBox)
listaOpciones['values'] = ('Hosts', 'Subredes')
listaOpciones.pack()
cantidadLbl = ttk.Label(ventana)
cantidadLbl.pack()
cantidadLbl['textvariable'] = opcionComboBox
hostsSubredes = tk.StringVar()
inputCantidad = ttk.Entry(ventana, textvariable=hostsSubredes)
inputCantidad.pack()
hostsLbl = ttk.Label(ventana, text="Hosts teóricos: ")
hostsLbl.pack()
hostsPracticosLbl = ttk.Label(ventana, text="Hosts prácticos: ")
hostsPracticosLbl.pack()
subredesLbl = ttk.Label(ventana, text="Subredes teóricas: ")
subredesLbl.pack()
subredesPracticasLbl = ttk.Label(ventana, text="Subredes prácticas: ")
subredesPracticasLbl.pack()
btnEjecutar = ttk.Button(ventana, text="Calcular")
btnEjecutar.pack()
# No quitar, es el ciclo principal del programa, es el que lo mantiene en ejecución
ventana.mainloop()

# Código principal
ip = input("Ingresa la dirección ip: ")
hosts = int(input("¿Cuántos hosts quieres por subred? "))
# Convierto el string que contiene la ip en un arreglo, tomando el punto como separador
ipArray = ip.split(".")
const = 256
# Creo un arreglo que contiene los numeros de la ip en enteros, para poder realizar operaciones sobre estos
ipNum = [int(x) for x in ipArray]
ipValida = True
# Comprueba si la ip es válida, itera sobre el arreglo y comprueba si el numero es menor que cero o mayor a 255
for i in range(0, len(ipNum)):
    if ipNum[i] < 0 or ipNum[i] > 255 or len(ipNum) != 4:
        ipValida = False
        break

# La clase la obtengo con el primer byte de la ip, en este caso está en el índice 0 del arreglo
clase = claseIp(ipNum[0])
maxHosts = hostsMaximos(clase)
exponente = math.ceil(math.log(hosts, 2))
logHosts = int(math.pow(2, exponente))
subredes = int(maxHosts / logHosts)
octeto = obtenerOcteto(clase)
salto = int(logHosts / const)
bits = bitsDisponibles(octeto)
# Variable auxiliar para acceder a los elementos del arreglo en el ciclo
j = -1
ipNumCopia = ipNum.copy()
hostcuenta = logHosts
k = 0
cociente = const / logHosts
mascara = obtenerMascara(clase)

if hosts > maxHosts or not ipValida:
    print("Compruebe el número de hosts o la dirección ip")
else:
    print("Dirección y número de hosts válidos")
    print(f"Hosts teóricos por subred disponibles: {logHosts}")
    print(f"Número de subredes teóricas: {subredes}")
    print(f"Número de hosts prácticos por subred disponibles: {logHosts - 2}")
    print(f"Número de subredes prácticas: {subredes - 2}")
    print(f"Clase: {clase}")
    print(f"Máscara por defecto: {mascara}")
    print(f"Nueva máscara:")
    if logHosts <= 2:
        print("Para configurar una red correctamente se requieren al menos 4 hosts por subred")
    else:
        if clase == "C":
            while octeto > 0:
                k += 1
                # Clase C funciona bien al 100%
                ipNumCopia[j] = ipNum[j] + logHosts - 1
                print(f"{k}.- Dirección de red: {'.'.join([str(x) for x in ipNum])}, "
                f"Rango de direcciones válidas: {str(ipNum[0]) + '.' + str(ipNum[1]) + '.' + str(ipNum[2]) + '.' + str(ipNum[j] + 1)}"
                f" - {str(ipNum[0]) + '.' + str(ipNum[1]) + '.' + str(ipNum[2]) + '.' + str(ipNumCopia[j] - 1)},"
                f" Dirección de broadcast: {'.'.join([str(x) for x in ipNumCopia])}")
                ipNum[j] += logHosts
                if ipNum[j] > 255:
                    octeto -= 1
        elif clase == "B":
            # Clase B funciona bien al 100%
            if logHosts < const:
                for k in range(0, subredes):
                    k += 1
                    ipNumCopia[j] = ipNum[j] + logHosts - 1
                    print(f"{k}.- {'.'.join([str(x) for x in ipNum])} - {'.'.join([str(x) for x in ipNumCopia])}")
                    ipNum[j] += logHosts
                    if ipNumCopia[j] >= 255:
                        j -= 1
                        ipNum[j] += 1
                        ipNumCopia[j] += 1
                        ipNum[j + 1] = 0
                        j += 1
                    elif ipNum[-1] > 255 and ipNum[-2] > 255:
                        octeto -= 2
            else:
                ipNumCopia[j] = 255
                ipNumCopia[j - 1] = salto - 1
                j -= 1
                for k in range(0, subredes):
                    k += 1
                    print(f"{k}.- {'.'.join([str(x) for x in ipNum])} - {'.'.join([str(x) for x in ipNumCopia])}")
                    ipNum[j] += salto
                    ipNumCopia[j] += salto
        elif clase == "A":
            # Clase A funciona al 100, o eso creo, depurenla más, pero la probé con 5 direcciones y las calculó bien
            # j = 3
            while octeto > 0:
                k += 1
                for hostcuenta in range(logHosts - 1):
                    ipNumCopia[j] += 1
                    hostcuenta -= 1
                    if ipNumCopia[3] > 255:
                        ipNumCopia[2] += 1
                        ipNumCopia[3] = 0
                    if ipNumCopia[2] > 255:
                        ipNumCopia[1] += 1
                        ipNumCopia[2] = 0
                    if ipNumCopia[1] == 255 and ipNumCopia[2] == 255 and ipNumCopia[3] == 255:
                        octeto = 0
                print(f"{k}.- {'.'.join([str(x) for x in ipNum])} - {'.'.join([str(x) for x in ipNumCopia])}")
                ipNum = ipNumCopia.copy()
                ipNum[3] += 1
                if ipNum[3] > 255:
                    ipNum[2] += 1
                    ipNum[3] = 0
                if ipNum[2] > 255:
                    ipNum[1] += 1
                    ipNum[2] = 0
                ipNumCopia = ipNum.copy()

