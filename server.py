import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid

from time import time

import cv2
from aiohttp import web
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder
import aiohttp_cors
import sqlconnector, sqls

from FaceRecognition.train import train_model, recorgn_face, initialize_face_recogn

ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")
pcs = set()

NUM_IMGS = 66
PATH_FACES = 'FaceRecognition/data/'
os.makedirs(PATH_FACES, exist_ok=True)

class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, passed, user_name, is_register):
        super().__init__()  # don't forget this!
        self.track = track
        # self.counter = 0
        self.is_register = is_register
        if not is_register:
            initialize_face_recogn()
        self.passed = passed
        self.user_ref = user_name
        self.user_name = user_name[0]
        self.time = time()
        if self.user_name != None and not os.path.exists(PATH_FACES + self.user_name):
            os.mkdir(PATH_FACES + self.user_name)
        self.cnt = 1

    async def recv(self):
        frame = await self.track.recv()
        if self.user_name == None:
            self.user_name = self.user_ref[0]
            if self.user_name != None and not os.path.exists(PATH_FACES + self.user_name):
                os.mkdir(PATH_FACES + self.user_name)
            # return new_frame
        img = frame.to_ndarray(format='bgr24')
        if self.is_register:
            if self.cnt <= NUM_IMGS:
                print(frame)
                print(f"w: {frame.width} h: {frame.height} format: {frame.format}")
                cv2.imwrite("{}{}/{}{:03d}.jpg".format(PATH_FACES, self.user_name, self.user_name, self.cnt), img)
                self.cnt += 1
            elif len(self.passed) == 0:
                print("Change State")
                self.passed.append(None)
        else:
            new_frame = recorgn_face(img)
            if type(new_frame) is tuple:
                name, new_frame = new_frame
                if len(self.passed) == 0:
                    sqls.insertLoginHistory(name)
                    print(name)
                    self.passed.append(name)
                    
            # new_frame = cv2.cvtColor(new_frame, cv2.COLOR_GRAY2RGB)
            new_frame = VideoFrame.from_ndarray(new_frame, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            frame = new_frame
        return frame

async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)

async def logo(request):
    # content = open(os.path.join(ROOT, "logo.png"), "r").read()
    return web.FileResponse('./logo.png')

async def indexjs(request):
    return await javascript(request, 'index.js')

async def rtcjs(request):
    return await javascript(request, 'RTCserver_connection.js')
    
async def javascript(request, file):
    content = open(os.path.join(ROOT, file), "r").read()
    return web.Response(content_type="application/javascript", text=content)

def sendDictAsJSON(func):
    def inner(request):
        return web.json_response(func(request))
    return inner

def getPostData(func):
    async def inner(request):
        post_data = await request.json()
        print(post_data)
        return func(post_data)
    return inner

@sendDictAsJSON
def show_info(request):
    records = sqls.getInfo()
    if len(records) >= 2:
        first, second = records
        return {'username': first[1], 'current': first[0], 'previous': second[0]}
    else:
        # No enough login history
        return {}

@getPostData
@sendDictAsJSON
def check(post_data):
    return {'exist': sqls.checkDuplicateUser(post_data['username'])}

@getPostData
@sendDictAsJSON
def test2(post_data):
    return post_data

@getPostData
@sendDictAsJSON
def insertUser(post_data):
    sqls.register(post_data['username'], post_data['password'])
    user_in_db = sqls.checkDuplicateUser(post_data['username'])
    if user_in_db:
        sqls.insertLoginHistory(post_data['username'])
    return {'registered': user_in_db}

@getPostData
@sendDictAsJSON
def password_login(post_data):
    return {'loginSucceed': sqls.loginWithPassword(post_data['username'], post_data['password'])}

async def register(request):  return await offer(request, True)

async def login(request):  return await offer(request, False)

async def offer(request, is_register):
    passed = []
    user_name = [None]
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.remote)

    # prepare local media
    # player = MediaPlayer(os.path.join(ROOT, "demo-instruct.wav"))
    if args.write_audio:
        recorder = MediaRecorder(args.write_audio)
    else:
        recorder = MediaBlackhole()  # 'what.mp4', options={'width': 1280, 'height':720}

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        async def on_message(message):
            if isinstance(message, str):
                if message.startswith("User "):
                    print('===')
                    username = message[5:]
                    user_name[0] = username
                    channel.send("You are " + username)
                    channel.send("Passed "+ str(len(passed) > 0))
                elif message.startswith('log'):
                    channel.send("Passed "+ str(len(passed) > 0))
                    print("=================")
                elif message.startswith("check"):
                    isPass = len(passed) > 0
                    print('[][]', isPass, passed)
                    while isPass != True:
                        await asyncio.sleep(1)
                        isPass = len(passed) > 0
                        print(isPass)
                    channel.send("Passed "+ str(isPass))
                elif message.startswith('train?'):
                    if await train_model():
                        channel.send('Trained')
                        print('Sent Trained to Client')
                else:
                    print("No matched message: ", message)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        log_info("ICE connection state is %s", pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        # if track.kind == "audio":
        #     pc.addTrack(player.audio)
        #     recorder.addTrack(track)
        if track.kind == "video":
            print("\nPreparing to cap picture from video\n")
            local_video = VideoTransformTrack(
                track, passed, user_name, is_register
            )
            pc.addTrack(local_video)

        @track.on("ended")
        async def on_ended():
            # print("Finished")
            log_info("Track %s ended", track.kind)
            await recorder.stop()
            # pc.close()
            # pcs.discard(pc)
            # return web.Response(
            #     content_type="application/json",
            #     text=json.dumps(
            #         {"userid": 11, "status": 'succeed'}
            #     ),
            # )

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )

async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="WebRTC audio / video / data-channels demo"
    )
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--verbose", "-v", action="count")
    parser.add_argument("--write-audio", help="Write received audio to a file")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None

    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    # ws_serve()
    app.router.add_get("/", index)
    app.router.add_get("/logo.png", logo)
    app.router.add_get("/index.js", indexjs)
    app.router.add_get("/RTCserver_connection.js", rtcjs)
    app.router.add_get("/test", sqlconnector.selection)
    app.router.add_get("/myInfo", show_info)
    # app.router.add_post("/offer", offer)
    app.router.add_post("/check", check)
    app.router.add_post("/register", register)
    app.router.add_post("/insert", insertUser)
    app.router.add_post("/password_login", password_login)
    app.router.add_post("/login", login)
    app.router.add_post("/test2", test2)

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                # allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app, access_log=None, port=args.port, ssl_context=ssl_context)

