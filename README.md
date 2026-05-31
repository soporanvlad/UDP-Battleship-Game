# UDP Battleship Game

A Battleship-style network game implemented using UDP communication between a Python client and either a Python or Node.js server.

## Overview

This project demonstrates UDP socket communication through a simplified Battleship game. Two devices communicate over a local network and take turns attacking enemy coordinates until one fleet is completely destroyed.

The project includes:

- Python UDP Client
- Python UDP Server
- Node.js UDP Server
- Battleship game logic
- Local network communication

## Technologies

- Python
- Node.js
- UDP Sockets
- NumPy

## Game Rules

Each player starts with a 10×10 game board.

Before the game begins:

- Each player places their ships on the board.
- Ships occupy multiple cells depending on their size.
- Players take turns attacking enemy coordinates.

For every attack, one of the following responses is returned:

- **Hit** – a ship segment was hit.
- **Miss** – no ship was hit.
- **Sunk** – all segments of a ship have been destroyed.
- **GAME OVER** – all enemy ships have been sunk.

A ship is considered sunk when all of its segments have been hit.

The winner is the player who sinks all enemy ships first.

## Ship Types

| Ship | Size |
|--------|--------|
| Portavion (Aircraft Carrier) | 5 |
| Crucisator (Cruiser) | 4 |
| Distrugator (Destroyer) | 3 |
| Submarin (Submarine) | 2 |
| Torpilor (Patrol Boat) | 1 |

## Project Structure

```text
.
├── udp_client.py
├── udp_server.py
├── udp_server.js
├── README.md
├── requirements.txt
└── .gitignore
```

## Network Configuration

### Python Client

Before running the client, configure:

```python
SERVER_IP = "SERVER-IP-HERE"
SERVER_PORT = 5555
```

Replace `SERVER-IP-HERE` with the IP address of the machine running the server.

### Server

Default server configuration:

```text
Host: 0.0.0.0
Port: 5555
```

## Running the Project

### Start the Python Server

```bash
python udp_server.py
```

### OR Start the Node.js Server

```bash
node udp_server.js
```

### Start the Client

```bash
python udp_client.py
```

## Example Messages

```text
3 5
Miss!
Hit Submarin !
Submarin sunk !
GAME OVER
```

## Notes

This project was developed as a networking exercise demonstrating UDP communication, game state management and interoperability between Python and Node.js applications.

Since UDP is connectionless, message delivery is not guaranteed. Client-side timeouts are used to handle communication issues.

## Author

Vlad Soporan
