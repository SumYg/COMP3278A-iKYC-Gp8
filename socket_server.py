#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets

# async def consumer(message):
#     print(message)
#     message.play()

async def time(websocket, path):
    # async for message in websocket:
    #     await consumer(message)
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(now)
        await asyncio.sleep(random.random() * 6.8)

# async def main(loop):
    # async with websockets.serve(time, "localhost", 5678):
        # await asyncio.Future()  # run forever
    # loop.

def ws_serve():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(time, "localhost", 5678))
    # asyncio.run(main())


