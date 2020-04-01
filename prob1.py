from numaleatorios import Aleatorio

random  = Aleatorio()

class Evento():

    def __init__(self):
        super().__init__()
        self.tipo_evento = ""
        self.tiempo_creacion = 0
        self.tiempo_salida = 0

#Simulacion en minutos

## Creacion de llegadas
tiempo = 0
tiempo_max = 6000

#Total de piezas que entraron en el sistema
totalPiezas = 0

#Total de dinero del sistema
totalCost = 0
tiempoUso = 0

eventos = []
# while(tiempo < tiempo_max):
def siguiente_llegada(tiempo):
    evento = Evento()
    evento.tiempo_creacion = tiempo + random.exponencial(0.7317/60)
    evento.tiempo_evento = evento.tiempo_creacion
    evento.tipo_evento = "llegada"
    # tiempo = evento.tiempo_creacion
    # totalPiezas += 1
    return evento


eventos.append(siguiente_llegada(0))
totalPiezas += 1

## Inicio de la simulacion 
tiempo = 0
cola_de_espera = []
salidas = []
troqueladoras = [False,False,False,False,False,False,False]
inspector_ocupado = False

piezas_max = 0

def asignarTroqueladora ():
    num = -1
    for idx, troqueladora in enumerate(troqueladoras):
        if troqueladora == False:
            num = idx
            break
    return num

def disponibilidad ():
    disponible = False
    for troqueladora in troqueladoras:
        if troqueladora == True:
            disponible = True
        else:
            disponible = False
    return disponible

while(tiempo < tiempo_max):
    eventos.sort(key=lambda x:x.tiempo_evento)
    evento = eventos.pop(0) ## Evento proximo
    tiempo = evento.tiempo_evento
    # print(evento.tiempo_evento, evento.tipo_evento, evento.tiempo_creacion)
    piezas_max = max(piezas_max, len(cola_de_espera))
    if(evento.tipo_evento == "llegada"):
        eventos.append(siguiente_llegada(tiempo))
        totalPiezas += 1
        if(len(cola_de_espera) == 0 and disponibilidad() == False):
            numTroqueladora = asignarTroqueladora()
            troqueladoras[numTroqueladora] = True
            evento.troqueladora = numTroqueladora
            evento.tiempo_inspeccion = tiempo
            evento.tiempo_evento = tiempo + 0.0833 ##Tiempo de inspección 
            evento.tipo_evento ="salida_inspeccion"
            evento.tiempo_salida = evento.tiempo_evento
            eventos.append(evento)
        else:
            cola_de_espera.append(evento)
    elif( evento.tipo_evento == "salida_inspeccion"):
        troqueladoras[evento.troqueladora] = False
        evento.tiempo_salida = tiempo
        salidas.append(evento)
        if(len(cola_de_espera)>0):
            pieza = cola_de_espera.pop(0)
            troqueladoras[evento.troqueladora] = False
            pieza.tiempo_inspeccion = tiempo
            pieza.troqueladora = evento.troqueladora
            pieza.tiempo_evento = tiempo + 0.0833 ##Tiempo de inspección 
            pieza.tiempo_salida = pieza.tiempo_evento
            pieza.tipo_evento ="salida_inspeccion"
            eventos.append(pieza)

tiempo_total_inspeccion = 0

for pieza in salidas:
    tiempo_total_inspeccion += pieza.tiempo_salida-pieza.tiempo_inspeccion

print("Total de piezas en el sistema: " + str(totalPiezas)) #total de piezas en el sistema
print("Tiempo promedio de piezas en el sistema: " + str(tiempo_total_inspeccion/totalPiezas))
print("Costo total: $" + str((tiempo_total_inspeccion/60)*10)) #el costo es de 10 dolares*hora de uso de troqueladora