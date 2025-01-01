#!/usr/bin/python3
# Using MIT License.
# https://github.com/bddjr/Minecraft-Server-Maintaining
#
# Tested version:
#  - Python: 3.12.5
#  - Minecraft: 1.21.4 1.12.2 1.8.9
# ------

# Config
ADDR = ("", 25565)
DESCRIPTION_TEXT = "§c服务器正在维护\nServer Maintaining"
DESCRIPTION_VERSION = "Server Maintaining"
JOIN_ERROR = "§c服务器正在维护\nServer Maintaining"

# ------

import socket, socketserver, json

print(f"127.0.0.1:{ADDR[1]}\nPress Ctrl+C to stop.")

description = json.dumps(
    {
        "description": {"text": DESCRIPTION_TEXT},
        "players": {"max": 0, "online": 0},
        "version": {"name": DESCRIPTION_VERSION, "protocol": 0},
    }
).encode("utf-8")

description = bytes([len(description) + 3, 1, 0, len(description), 1]) + description

joinError = json.dumps(JOIN_ERROR).encode("utf-8")

joinError = bytes([len(joinError) + 2, 0, len(joinError)]) + joinError


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        c: socket.socket = self.request
        c.settimeout(5)
        packetLen = c.recv(1)[0]
        data = c.recv(packetLen)
        socketType = data[packetLen - 1]
        if socketType == 1:
            # ping
            c.recv(2)
            c.send(description)
            data = c.recv(10)
            c.send(data)
        elif socketType == 2:
            # join
            c.recv(256)
            c.send(joinError)


srv = socketserver.ThreadingTCPServer(ADDR, Handler)

try:
    srv.serve_forever()
except KeyboardInterrupt:
    pass
