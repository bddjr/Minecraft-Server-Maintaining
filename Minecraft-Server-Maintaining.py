# Config
ADDR = ("", 25565)
DESCRIPTION_TEXT = "§c服务器正在维护\nServer Maintaining"
DESCRIPTION_VERSION = "Server Maintaining"
CONNECTION_ERROR = "§c服务器正在维护\nServer Maintaining"

# ------
# Using MIT License.
# https://github.com/bddjr/Minecraft-Server-Maintaining
#
# Tested version:
#  - Python: 3.12.5
#  - Minecraft: 1.21.4 1.12.2 1.8.9
# ------

import socket, socketserver, json

print(f"127.0.0.1:{ADDR[1]}")

description = json.dumps(
    {
        "description": {"text": DESCRIPTION_TEXT},
        "players": {"max": 0, "online": 0},
        "version": {"name": DESCRIPTION_VERSION, "protocol": 0},
    }
).encode("utf-8")

description = bytes([len(description) + 3, 1, 0, len(description), 1]) + description

connectionError = json.dumps(CONNECTION_ERROR).encode("utf-8")

connectionError = (
    bytes([len(connectionError) + 2, 0, len(connectionError)]) + connectionError
)


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        c: socket.socket = self.request
        c.settimeout(5)
        packetLen = c.recv(1)[0]
        data = c.recv(packetLen)
        match data[packetLen - 1]:
            case 1:
                # ping
                c.recv(2)
                c.send(description)
                data = c.recv(10)
                c.send(data)
            case 2:
                # join
                c.recv(256)
                c.send(connectionError)


srv = socketserver.ThreadingTCPServer(ADDR, Handler)
srv.serve_forever()
