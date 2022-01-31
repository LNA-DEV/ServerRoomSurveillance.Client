import socketserver
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from typing import Tuple


class ServerRoomHTTPHandler(BaseHTTPRequestHandler):
    room = 0
    temp = 0
    humid = 0
    tlimit = 0
    hlimit = 0

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)
        print(self.path)
        print(self.server)

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open("WebPage/HTML/index.html", "rb")
            page = file.read()
            self.wfile.write(page)

        if self.path == "/data_request.js":
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.end_headers()
            file = open("WebPage/Scripts/index.js", "rb")
            js = file.read()
            self.wfile.write(js)

        if self.path == "/Styles/index.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            file = open("WebPage/Styles/index.css", "rb")
            css = file.read()
            self.wfile.write(css)

        if self.path == "/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            # data = json.dumps('{"room": 113, "temp": 25, "humid": 75}')
            data = json.dumps('{"room":' + str(ServerRoomHTTPHandler.room) + ', "temp":' + str(
                ServerRoomHTTPHandler.temp) + ', "humid":' + str(ServerRoomHTTPHandler.humid) + ', "tlimit":' + str(
                ServerRoomHTTPHandler.tlimit) + ', "hlimit":' + str(ServerRoomHTTPHandler.hlimit) + '}')
            self.wfile.write(bytes(data, "utf-8"))

    @staticmethod
    def run(hostName, serverPort):
        webserver = HTTPServer((hostName, serverPort), ServerRoomHTTPHandler)
        t = threading.Thread(target=webserver.serve_forever)
        t.start()
        print("Webserver started http://%s:%s" % (hostName, serverPort))



# Standalone webserver starter
if __name__ == "__main__":
    testserver = HTTPServer(("localhost", 1111), ServerRoomHTTPHandler)
    threading.Thread(target=testserver.serve_forever).start()
    print("Testserver started http://%s:%s" % ("localhost", "1111"))
