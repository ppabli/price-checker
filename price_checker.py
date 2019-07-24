import requests
from bs4 import BeautifulSoup
import mysql.connector
import sys
sys.path.append("..")
import config

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

opciones = {"Añadir tracker", "Ver trackers"}

def mostrarOpciones ():
    print("Tenemos estas opciones: ")
    contador = 0
    for x in opciones:
        print(contador, " - ", x)
        contador = contador + 1
    print("Que opcion quiere:", end = " ")

def añadirTracker ():
    url = input("Introduzca la URL que quiere añadir: ")
    page = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    title = soup2.find(id="productTitle").get_text().strip()
    price = soup2.find(id="priceblock_ourprice").get_text().strip()
    converted_price = price[0:5]

    try:
        mydb = mysql.connector.connect (
            host = config.host,
            user = config.user,
            passwd = config.passwd,
            database = config.database
        )
    except:
        return print("Error al conectar con la base de datos. No se ha guardado el nuevo tracker")
    finally:
        try:
            cursor = mydb.cursor()
            sql = "insert into trackers values (%s, %s, %s, %s, %s, %s, %s)"
            val = (0, title, url, converted_price, 0, 0, 0)
            cursor.execute(sql, val)
            mydb.commit()
            print("Se ha añadido el nuevo tracker")
        except:
            return print("Error al guardar el nuevo tracker")
        finally:
            if(mydb.is_connected()):
                mydb.close()

def verTrackers ():
    print("Tenemos estos trackers: ")


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