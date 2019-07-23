
opciones = {"Añadir tracker", "Ver trackers"}
trackers = {}

def mostrarOpciones ():
    print("Tenemos estas opciones: ")
    contador = 0
    for x in opciones:
        print(contador, " - ", x)
        contador = contador + 1
    print("Que opcion quiere:", end=" ")

def añadirTracker ():
    print("Introduzca la URL que quiere añadir", end=" ")
    url = input()

def verTrackers ():
    print("Tenemos estos trackers: ")
    contador = 0
    for x in trackers:
        print(contador, " - ", x)
        contador = contador + 1
    print(" ")

print("Bienvenido a price tracker")
while True:
    mostrarOpciones()
    opcion = int(input())
    if opcion == 0:
        verTrackers()
    elif opcion == 1:
        añadirTracker()
    elif opcion == -1:
        break