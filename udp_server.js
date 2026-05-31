const dgram = require("dgram");

const HOST = "0.0.0.0";
const PORT = 5555;
const BUFF = 1024;

function coord(x, y) { return `${x},${y}`; }

const torpilor = new Set([coord(0,2), coord(0,3)]);
const submarin = new Set([coord(8,6), coord(8,7), coord(8,8)]);
const distrugator = new Set([coord(3,2), coord(4,3), coord(5,4)]);
const crucisator = new Set([coord(8,1), coord(8,2), coord(8,3), coord(8,4)]);
const portavion = new Set([coord(2,8), coord(3,8), coord(4,8), coord(5,8), coord(6,8)]);

const ships = {
    Torpilor: torpilor,
    Submarin: submarin,
    Distrugator: distrugator,
    Crucisator: crucisator,
    Portavion: portavion
};

let hits = {};
for (const name in ships) hits[name] = new Set();

let enemyHits = new Set();
const shipsTotal = Object.keys(ships).length;
let shipsSunk = 0;

const server = dgram.createSocket("udp4");
console.log(`Server UDP ascultă pe ${HOST}:${PORT}`);

let clientAddr = null;
let clientPort = null;
let gameOver = false;

server.on("message", (msg, rinfo) => {
    const text = msg.toString().trim();

    if (!clientAddr) {
        clientAddr = rinfo.address;
        clientPort = rinfo.port;
        console.log("Clientul conectat:", clientAddr, clientPort);
        return;
    }

    if (text === "GAME OVER") {
        console.log("Server-ul a castigat !");
        gameOver = true;
        return;
    }

    const parts = text.split(" ");
    if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
        const [cx, cy] = parts.map(Number);
        const ccoord = coord(cx, cy);

        let response = "Miss!";
        for (const name in ships) {
            if (ships[name].has(ccoord)) {
                hits[name].add(ccoord);
                response = hits[name].size === ships[name].size ? `${name} sunk !` : `Hit ${name} !`;
                if (hits[name].size === ships[name].size) shipsSunk += 1;
                break;
            }
        }

        if (shipsSunk === shipsTotal) {
            response = "GAME OVER";
            gameOver = true;
        }

        server.send(response, clientPort, clientAddr);
        console.log(`Clientul loveste: (${cx},${cy}), Raspuns: ${response}`);

        if (!gameOver) {
            let x, y;
            do {
                x = Math.floor(Math.random() * 10);
                y = Math.floor(Math.random() * 10);
            } while (enemyHits.has(coord(x, y)));

            enemyHits.add(coord(x, y));

            const shot = `${x} ${y}`;
            server.send(shot, clientPort, clientAddr);
            console.log(`Server loveste: ${x},${y}`);
        }
    } else {
        console.log("Mesaj client invalid:", text);
    }
});

server.bind(PORT, HOST);
