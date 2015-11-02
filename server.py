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
    dicserv ={}
    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        #self.wfile.write(b"Hemos recibido tu peticion")
        IP = self.client_address[0]
        PORT = self.client_address[1]
        print("IP: ", IP)#Lo que tiene mi clnt con self.cl..
        print("Puerto: ",PORT )

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            lineb = self.rfile.read()
            print("El cliente nos manda " + lineb.decode('utf-8'))
            line = lineb.decode('utf-8')
            if not line:  # Si no hay más líneas salimos del bucle infinito
                break
            (metodo, direccion, elresto, expire, valor) = line.split()
            if metodo != "REGISTER" and not "@" in direccion:
                break
            if int(valor) == 0:
                del self.dicserv[direccion]
                self.wfile.write(b"SIP/2.0 200 OK")
                print(self.dicserv)
            else:
                USER = direccion.split(":")[1]
                self.dicserv[direccion] = [IP ,valor]
                self.wfile.write(b"SIP/2.0 200 OK"+b"\r\n"+b"\r\n")
                print (self.dicserv)
if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
