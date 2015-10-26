#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """


    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion")
        print("IP: ",self.client_address[0])#Lo que tiene mi clnt con self.cl..
        print("Puerto: ", self.client_address[1])
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            lineb = self.rfile.read()
            print("El cliente nos manda " + lineb.decode('utf-8'))
            line = lineb.decode('utf-8')
            if not line:  # Si no hay más líneas salimos del bucle infinito
                break
            (metodo, direccion, elresto) = line.split()
            print(metodo, direccion, elresto)
            if metodo != "REGISTER" or not "@" in direccion:
                break
            USER = direccion.split(":")[1]
            print(USER)


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
