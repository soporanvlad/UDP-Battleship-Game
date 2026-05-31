
import socket
import numpy as np
import random

#conexiune
SERVER_IP = "SERVER-IP-HERE"  
SERVER_PORT = 5555
BUFF = 1024

# Torpilor
torpilor = {(1, 1), (1, 2)}

# Submarin
submarin = {(5, 0), (6, 0), (7, 0)}

# Distrugator
distrugator = {(3, 6), (3, 7), (3, 8)}

# Crucisator
crucisator = {(0, 9), (1, 9), (2, 9), (3, 9)}

# Portavion
portavion = {(9, 2), (9, 3), (9, 4), (9, 5), (9, 6)}

ships = {
    "Torpilor": torpilor,
    "Submarin": submarin,
    "Distrugator": distrugator,
    "Crucisator": crucisator,
    "Portavion": portavion
}

hits = {name: set() for name in ships}
enemy_hits = set()
ships_total = len(ships)
ships_sunk = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)
try:
    s.sendto(b"ready(windows)", (SERVER_IP, SERVER_PORT))
    game_over = False
    while not game_over:
        try:
            data, _ = s.recvfrom(BUFF)
            msg = data.decode()
            sx, sy = map(int, msg.split())
            coord = (sx, sy)

            response = "Miss!"
            for name, ships_coords in ships.items():
                if coord in ships_coords:
                    hits[name].add(coord)
                    response = f"Hit {name} !"
                    if hits[name] == ships_coords:
                        ships_sunk += 1
                        response = f"{name} sunk !"
                    break
            if ships_sunk == ships_total:
                response="GAME OVER"
                game_over = True
        
            s.sendto(response.encode(), (SERVER_IP, SERVER_PORT))
            print(f"Server loveste: {coord}, Raspuns client: {response}")

            if response == "GAME OVER":
                print("Clientul a pierdut!")
                break
        except socket.timeout:
            print("Timeout: nu am primit răspuns")
    
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if (x, y) not in enemy_hits:
                enemy_hits.add((x, y))
                break
    
        msg = f"{x} {y}".encode()
        s.sendto(msg, (SERVER_IP, SERVER_PORT))
        print(f"Clientul loveste: {x}, {y}")

        try:
            data, _ = s.recvfrom(BUFF)
            resp = data.decode()
            print("Raspuns server: ", resp)
            if resp == "GAME OVER":
                print("Clientul a castigat!")
                break
        except socket.timeout:
            print("Timeout la asteptarea raspunsului serverului")
except KeyboardInterrupt:
    print("Client oprit")
finally:
    s.close()
