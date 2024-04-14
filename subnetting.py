import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

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

# Devuelve la representación en binario en 8 bits e.g. = 10 = 00001010
def decimalABinario(numero):
    binario = format(numero, 'b')
    binario8bits = binario.zfill(8)
    return binario8bits

# El parámetro de máscara se pasa en binario
def nuevaMascara(octeto, subredes, mascara):
    # Para que calcule correctamente la máscara esta se debe de pasar como arreglo
    # La máscara no se pasa en decimal
    # Todo el proceso con la máscara se lleva a cabo en binario
    posicion = (octeto * 8) * -1
    bitsSubred = int(math.log(subredes,2))
    # Ciclo que inserta los bits usados en la subred desde la derecha individualmente
    for i in range(0, bitsSubred):
        mascara[posicion] = '1'
        posicion += 1
    mascara8bits = []
    # Este ciclo agrupa los elementos de 8 en 8 para que se agrupen por byte
    for i in range(0, len(mascara), 8):
        byte = mascara[i:i + 8]
        bytestr = "".join(map(str, byte))
        mascara8bits.append(bytestr)
    # Retorno el arreglo con las máscara ya calculada pero en entero para después convertirla a decimal
    return [int(x) for x in mascara8bits]

def binarioADecimal(numero):
    acumulador = 0
    k = -1
    numstr = str(numero)
    listaEnteros = [int(x) for x in numstr]
    for i in listaEnteros[::-1]:
        k += 1
        acumulador += (i*(2**k))
    return acumulador

def obtenerBits(clase):
    if clase == "C":
        return 8
    elif clase == "B":
        return 8 * 2
    elif clase == "A":
        return 8 * 3
    else:
        return "Error"

# Función para calcular y mostrar las direcciones IP
def calcularDirecciones():
    # Obtener los valores de la interfaz gráfica
    ip = str(direccion.get())
    cantidad = int(hostsSubredes.get())

    # Proceso de cálculo
    ipArray = ip.split(".")
    const = 256
    ipNum = [int(x) for x in ipArray]
    ipValida = True
    for i in range(0, len(ipNum)):
        if ipNum[i] < 0 or ipNum[i] > 255 or len(ipNum) != 4:
            ipValida = False
            break

    clase = claseIp(ipNum[0])
    maxHosts = hostsMaximos(clase)
    exponente = math.ceil(math.log(cantidad, 2))
    logHosts = int(math.pow(2, exponente))
    octeto = obtenerOcteto(clase)
    bits = obtenerBits(clase)
    exponenteSubredes = bits - exponente
    subredes = int(math.pow(2, exponenteSubredes))
    opcion = opcionComboBox.get()
    if opcion == "Subredes":
        a = subredes
        subredes = logHosts
        logHosts = a
    salto = int(logHosts / const)
    j = -1
    ipNumCopia = ipNum.copy()
    k = 0
    mascara = obtenerMascara(clase)
    mascaraArray = mascara.split('.')
    mascaraInt = [int(x) for x in mascaraArray]
    mascaraBinario = list(map(decimalABinario, mascaraInt))
    mascaraInd = []
    for numero in mascaraBinario:
        mascaraInd.extend(numero)
    mascaraNueva = nuevaMascara(octeto, subredes, mascaraInd)
    mascaraDecimal = list(map(binarioADecimal, mascaraNueva))
    # Mostrar el resultado en el widget de texto
    direccionesTexto.delete('1.0', tk.END)  # Borrar el contenido anterior

    if cantidad > maxHosts or not ipValida:
        messagebox.showerror("Error", "Compruebe el número de hosts/subredes o la dirección IP")
    else:
        hostsLbl.config(text=f"Número de hosts teóricos disponibles: {logHosts}")
        hostsPracticosLbl.config(text=f"Número de hosts prácticos disponibles: {logHosts - 2}")
        subredesLbl.config(text=f"Número de subredes teóricas disponibles: {subredes}")
        subredesPracticasLbl.config(text=f"Número de subredes prácticas disponibles: {subredes - 2}")
        mascaraLbl.config(text=f"Máscara: {mascara}")
        nuevaMascaraLbl.config(text=f"Nueva máscara: {'.'.join([str(x) for x in mascaraDecimal])}")
        claseLbl.config(text=f"Clase: {clase}")

        if logHosts <= 2 or subredes <= 2:
            messagebox.showerror("Error", "Para configurar una red correctamente se requieren al menos 4 hosts o subredes")
        else:
            if clase == "C":
                while octeto > 0:
                    k += 1
                    ipNumCopia[j] = ipNum[j] + logHosts - 1
                    direccion_red = '.'.join([str(x) for x in ipNum])
                    direccion_broadcast = '.'.join([str(x) for x in ipNumCopia])
                    rango_direcciones = f"{ipNum[0]}.{ipNum[1]}.{ipNum[2]}.{ipNum[j] + 1} - {ipNum[0]}.{ipNum[1]}.{ipNum[2]}.{ipNumCopia[j] - 1}"
                    direccionesTexto.insert(tk.END, f"{k}.- Dirección de red: {direccion_red}, Rango de direcciones válidas: {rango_direcciones}, Dirección de broadcast: {direccion_broadcast}\n")
                    ipNum[j] += logHosts
                    if ipNum[j] > 255:
                        octeto -= 1
            elif clase == "B":
                if logHosts <= const:
                    for k in range(0, subredes):
                        k += 1
                        ipNumCopia[j] = ipNum[j] + logHosts - 1
                        direccion_red = '.'.join([str(x) for x in ipNum])
                        direccion_broadcast = '.'.join([str(x) for x in ipNumCopia])
                        direccionesTexto.insert(tk.END, f"{k}.- {direccion_red} - {direccion_broadcast}\n")
                        ipNum[j] += logHosts
                        if ipNumCopia[j] >= 255:
                            j -= 1
                            ipNum[j] += 1
                            ipNumCopia[j] += 1
                            ipNum[j + 1] = 0
                            j += 1
                        elif ipNum[-1] > 255 and ipNum[-2] > 255:
                            octeto -= 2
                elif logHosts > const:
                    ipNumCopia[j] = 255
                    ipNumCopia[j - 1] = salto - 1
                    j -= 1
                    for k in range(0, subredes):
                        k += 1
                        direccion_red = '.'.join([str(x) for x in ipNum])
                        direccion_broadcast = '.'.join([str(x) for x in ipNumCopia])
                        direccionesTexto.insert(tk.END, f"{k}.- {direccion_red} - {direccion_broadcast}\n")
                        ipNum[j] += salto
                        ipNumCopia[j] += salto
            elif clase == "A":
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
                    direccion_red = '.'.join([str(x) for x in ipNum])
                    direccion_broadcast = '.'.join([str(x) for x in ipNumCopia])
                    direccionesTexto.insert(tk.END, f"{k}.- {direccion_red} - {direccion_broadcast}\n")
                    ipNum = ipNumCopia.copy()
                    ipNum[3] += 1
                    if ipNum[3] > 255:
                        ipNum[2] += 1
                        ipNum[3] = 0
                    if ipNum[2] > 255:
                        ipNum[1] += 1
                        ipNum[2] = 0
                    ipNumCopia = ipNum.copy()

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
listaOpciones = ttk.Combobox(ventana, textvariable=opcionComboBox, state="readonly")
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
mascaraLbl = ttk.Label(ventana, text="Máscara: ")
mascaraLbl.pack()
nuevaMascaraLbl = ttk.Label(ventana, text="Nueva máscara: ")
nuevaMascaraLbl.pack()
claseLbl = ttk.Label(ventana, text="Clase: ")
claseLbl.pack()
btnEjecutar = ttk.Button(ventana, text="Calcular", command=calcularDirecciones)
btnEjecutar.pack()
direccionesTexto = ScrolledText(ventana, width=150, height=20, wrap=tk.WORD)
direccionesTexto.pack()
# No quitar, es el ciclo principal del programa, es el que lo mantiene en ejecución
ventana.mainloop()
