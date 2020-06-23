import requests
import threading
import time
from bs4 import BeautifulSoup
import mysql.connector
import sys

sys.path.append("..")
import config
import smtplib

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

opciones = {
    -1: "Salir",
    0: "Añadir tracker",
    1: "Ver todos los trackers",
    2: "Ver trackers activos",
    3: "Ver trackers terminados",
    4: "Ver trackers pausados",
    5: "Trackear precios ahora",
    6: "Iniciar trackers automaticos",
    7: "Cambiar precio deseado",
    8: "Cambiar estado"
}

estados = {
    0: "",
    1: "activo",
    2: "pausado",
    3: "terminado",
    4: "notificado"
}


def mostrarOpciones():
    print("Tenemos estas opciones: ")
    for x in opciones:
        print(x, " - ", opciones[x])
    print("Que opcion quiere:", end=" ")
    return


def añadirTracker():
    try:
        url = input("Introduzca la URL que quiere añadir: ")
        page = requests.get(url, headers=headers)
        soup1 = BeautifulSoup(page.content, 'html.parser')
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
        title = soup2.find(id="productTitle").get_text().strip()
        price = soup2.find(id="priceblock_ourprice").get_text().strip().replace(",", ".")
        converted_price = float(price[0:6])
    except:
        return print("Error al cargar la pagina para crear el tracker")
    finally:
        try:
            precio_deseado = float(input("Introduzca el precio al que desee comprar: "))
        except:
            return print("Error el precio deseado introducido no es correcto")
        finally:
            try:
                mydb = mysql.connector.connect(
                    host=config.host,
                    user=config.user,
                    passwd=config.passwd,
                    database=config.database
                )
            except:
                return print("Error al conectar con la base de datos. No se ha guardado el nuevo tracker")
            finally:
                try:
                    mycursor = mydb.cursor()
                    sql = "insert into trackers values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (0, title, url, converted_price, converted_price, precio_deseado, converted_price, converted_price, estados[1])
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("Se ha añadido el nuevo tracker")
                except:
                    return print("Error al guardar el nuevo tracker")
                finally:
                    if (mydb.is_connected()):
                        mydb.close()
                    return


def verTrackers(codigo_estado):
    try:
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            passwd=config.passwd,
            database=config.database
        )
        mycursor = mydb.cursor()
        sql = "select * from trackers"
        if codigo_estado != 0:
            sql = sql + f" where estado = '{estados[codigo_estado]}'"
            print(f"Tenemos estos trackers {estados[codigo_estado]}s:")
        else:
            print(f"Tenemos estos trackers:")
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            print(mycursor.column_names[0], "-", x[0])
            print(" |", mycursor.column_names[1], "-", x[1])
            print(" |", mycursor.column_names[2], "-", x[2])
            print(" |", mycursor.column_names[3], "-", x[3])
            print(" |", mycursor.column_names[4], "-", x[4])
            print(" |", mycursor.column_names[5], "-", x[5])
            print(" |", mycursor.column_names[6], "-", x[6])
            print(" |", mycursor.column_names[7], "-", x[7])
            print(" |", mycursor.column_names[8], "-", x[8])
            print("---------------------------")
        return
    except:
        return print("Error al leer los trackers almacenados en la base de datos")
    finally:
        if (mydb.is_connected()):
            mydb.close()
        return


def actualizar_precio(id, columna, nuevo_precio):
    try:
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            passwd=config.passwd,
            database=config.database
        )

        mycursor = mydb.cursor()
        sql = ""

        if columna == "precio_deseado":
            sql = "update trackers set precio_deseado = %s where id = %s and estado = %s"
        elif columna == "precio_actual":
            sql = "update trackers set precio_actual = %s where id = %s and estado = %s"
        elif columna == "precio_mas_bajo":
            sql = "update trackers set precio_mas_bajo = %s where id = %s and estado = %s"
        elif columna == "precio_mas_alto":
            sql = "update trackers set precio_mas_alto = %s where id = %s and estado = %s"

        val = (nuevo_precio, id, estados[1])
        mycursor.execute(sql, val)

        mydb.commit()
    except:
        return print("Error al actualizar el precio en la base de datos")
    finally:
        if (mydb.is_connected()):
            mydb.close()
        return


def send_email(id, titulo, url, precio_inicial, precio_actual, precio_deseado, precio_mas_bajo, precio_mas_alto):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login("ppabli12@gmail.com", config.googlepassword)

        subject = f"Bajada de precio del producto {titulo}"
        body = f"Este es un mensaje automatizado del price tracker. \nEl producto {titulo} con id: {id} ha bajado de precio y esta a {precio_actual} euros.\nRevisa el producto aqui: {url}\n"

        message = f"Subject: {subject}\n\n{body}".encode('utf-8')

        server.sendmail(
            "ppabli12@gmail.com",
            "ppabli12@gmail.com",
            message
        )
    except:
        return print("Error al mandar el email")
    finally:
        return server.quit()


def cambiar_precio_deseado():
    verTrackers()
    id = int(input("Que producto desea cambiar el precio deseado: "))
    precio_deseado = float(input("Que precio quieres poner: "))
    actualizar_precio(id, "precio_deseado", precio_deseado)
    return

def cambiar_estado(id, codigo_estado):
    try:
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            passwd=config.passwd,
            database=config.database
        )

        mycursor = mydb.cursor()
        sql = ("update trackers set estado = %s where id = %s")
        val = (estados[codigo_estado], id)
        mycursor.execute(sql, val)

        mydb.commit()
    except:
        return print("Error al actualizar el estado en la base de datos")
    finally:
        if (mydb.is_connected()):
            mydb.close()
        return

def trackear_precio():
    try:
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            passwd=config.passwd,
            database=config.database
        )

        mycursor = mydb.cursor()
        mycursor.execute(f"select * from trackers where estado = '{estados[1]}'")
        myresult = mycursor.fetchall()

        for x in myresult:
            url = x[2]
            page = requests.get(url, headers=headers)
            soup1 = BeautifulSoup(page.content, 'html.parser')
            soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
            price = soup2.find(id="priceblock_ourprice").get_text().strip().replace(",", ".")
            converted_price = float(price[0:6])

            if converted_price < x[6]:
                # cambiar el valor del precio mas bajo en la base de datos
                actualizar_precio(x[0], mycursor.column_names[6], converted_price)
            if converted_price > x[7]:
                # cambiar el valor del precio mas alto en la base de datos
                actualizar_precio(x[0], mycursor.column_names[7], converted_price)
            if converted_price != x[4]:
                # cambiar el valor del precio actual en la base de datos
                actualizar_precio(x[0], mycursor.column_names[4], converted_price)
            if converted_price <= x[5]:
                # mandar un mensaje porque el precio del producto es menor o igual al precio deseado
                send_email(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
                cambiar_estado(x[0], 4)
    except:
        return print("Error al tracker el precio")
    finally:
        if (mydb.is_connected()):
            mydb.close()
        return


class MyThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self.parar = False
        return

    def run(self):
        while self.parar != True:
            trackear_precio()
            contador = 0
            while self.parar == False and contador <= 1800:
                contador = contador + 1
                time.sleep(1)
        return

    def stop(self):
        self.parar = True
        return


thread = None
opcion = None
print("Bienvenido al price tracker")
while True:
    try:
        mostrarOpciones()
        opcion = int(input())
        if opcion == -1:
            if thread != None:
                thread.stop()
                thread.join()
            print("Chao")
            break;
            exit()
        if opcion == 0:
            añadirTracker()
        if opcion == 1:
            verTrackers(0)  # todos
        if opcion == 2:
            verTrackers(1)  # activos
        if opcion == 3:
            verTrackers(3)  # terminados
        if opcion == 4:
            verTrackers(2)  # pausado
        if opcion == 5:
            trackear_precio()
        if opcion == 6:
            if thread != None:
                print("Tracker automatico ya esta activado")
            else:
                thread = MyThread()
                thread.start()
                print("Tracker automatico activado")
        if opcion == 7:
            cambiar_precio_deseado()
    except:
        print("El valor introducido no es correcto")
        continue
