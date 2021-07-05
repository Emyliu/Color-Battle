#!/usr/bin/env python

# WS server example

import asyncio
import websockets
from board import Board
import json
import copy

websocket_clients = set()

b = Board(10,10,0,["R","O","Y","G","B","I"])


b.fill_with_color();

filled = [False, False]
d = {}

async def sendState(loop):
    while True:
        for c in websocket_clients:
            output = copy.deepcopy(b.output())

            for y in range(len(output)):
                for x in range(len(output[0])):
                    output[y][x] = [output[y][x].color, output[y][x].player]

            data = [output, d[c.remote_address], b.player_counts, b.last_moved, b.player_colors]

            await c.send(json.dumps(data))
        await asyncio.sleep(0.2)


async def registerConnection(websocket, path):
    global b
    print(websocket)
    global filled
    if len(websocket_clients) >= 2:
        d[websocket.remote_address] = 2
    else:
        player_id = 0
        if filled[0]:
            player_id = 1
        else:
            player_id = 0
        d[websocket.remote_address] = player_id
        filled[player_id] = True
    while True:
        await websocket.recv()
        websocket_clients.add(websocket)
        try:
            # This loop will keep listening on the socket until its closed. 
            async for raw_message in websocket:
                if raw_message == "Reset":
                    b = Board(10,10,0,["R","O","Y","G","B","I"])
                    b.fill_with_color();
                else:
                    print(f'Got: [{raw_message}] from socket [{id(websocket)}]')
                    color = raw_message[0]
                    player = int(raw_message[1])
                    b.fill(player, color)

        except websockets.exceptions.ConnectionClosedError as cce:
            websocket_clients.remove(websocket)
            if d[websocket.remote_address] < 2:
                filled[d[websocket.remote_address]] = False
            del d[websocket.remote_address]
        
        finally:
            print(f'Disconnected from socket [{id(websocket)}]...')
            websocket_clients.remove(websocket)
            if d[websocket.remote_address] < 2:
                filled[d[websocket.remote_address]] = False
            del d[websocket.remote_address]


loop = asyncio.get_event_loop()
start_server = websockets.serve(registerConnection, "localhost", 8765)
print(f'Started socket server: {start_server} ...')
loop.run_until_complete(start_server)
loop.run_until_complete(sendState(loop))
loop.run_forever()