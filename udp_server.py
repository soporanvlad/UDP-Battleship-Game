import socket
import random

#conexiune
HOST = "0.0.0.0"
PORT = 5555
BUFF = 1024

# Torpilor
torpilor = {(0, 2), (0, 3)}

# Submarin
submarin = {(8, 6), (8, 7), (8, 8)}

# Distrugator
distrugator = {(3, 2), (4, 3), (5, 4)}

# Crucisator
crucisator = {(8, 1), (8, 2), (8, 3), (8, 4)}

# Portavion
portavion = {(2, 8), (3, 8), (4, 8), (5, 8), (6, 8)}

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
s.bind((HOST, PORT))
print(f"Server UDP ascultă pe {HOST}:{PORT}")

try:
    print("Asteptam clientul sa intre in joc....")
    data, addr = s.recvfrom(BUFF)
    print("Clientul conectat:", addr)
    
    game_over = False
    while not game_over:
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if (x, y) not in enemy_hits:
                enemy_hits.add((x, y))
                break
        
        msg = f"{x} {y}".encode()
        s.sendto(msg, addr)
        print(f"Server loveste: {x},{y}")
        
        try:
            data, _ = s.recvfrom(BUFF)
            resp = data.decode()
            print("Raspuns client: ", resp)
            if resp == "GAME OVER":
                print("Server-ul a castigat !")
                break
        except socket.timeout:
            print("Timeout la asteptarea raspunsului clientului!")
        
        try:
            data, _ = s.recvfrom(BUFF)
            msg = data.decode()
            cx, cy = map(int, msg.split())
            coord = (cx, cy)

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
                response = "GAME OVER"
                game_over = True
            
            s.sendto(response.encode(), addr)
            print(f"Clientul loveste: {coord}, Raspuns: {response}")
        except Exception as e:
            print("Eroare:", e)

except KeyboardInterrupt:
    print("Oprire server")
finally:
    s.close()
