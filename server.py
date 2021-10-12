import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid

import cv2
from aiohttp import web
from av import VideoFrame

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder

from socket_server import ws_serve

ROOT = os.path.dirname(__file__)

logger = logging.getLogger("pc")
pcs = set()

NUM_IMGS = 100
class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform, passed, user_name):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform
        # self.counter = 0
        self.passed = passed
        self.user_ref = user_name
        self.user_name = user_name[0]
        if self.user_name != None and not os.path.exists('data/{}'.format(self.user_name)):
            os.mkdir('data/{}'.format(self.user_name))
        self.cnt = 1
        

    async def recv(self):
        frame = await self.track.recv()
        if self.user_name == None:
            img = frame.to_ndarray(format='bgr24')
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            # print(self.user_ref)
            self.user_name = self.user_ref[0]
            new_frame = VideoFrame.from_ndarray(cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB), format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            if self.user_name != None and not os.path.exists('data/{}'.format(self.user_name)):
                os.mkdir('data/{}'.format(self.user_name))
            return new_frame
        if self.cnt <= NUM_IMGS:
            # await stop_this_connection(self.pc)
            # await self.track.stop()
            # return
            # print(type(frame))
            # gray = cv2.cvtColor(frame.to_ndarray(format='bgr24'), cv2.COLOR_BGR2GRAY)
            img = frame.to_ndarray(format='bgr24')
            cv2.imwrite("data/{}/{}{:03d}.jpg".format(self.user_name, self.user_name, self.cnt), img)
            self.cnt += 1
            # self.passed.append(None)
        return frame
        # if self.transform == "cartoon":
        #     img = frame.to_ndarray(format="bgr24")

        #     # prepare color
        #     img_color = cv2.pyrDown(cv2.pyrDown(img))
        #     for _ in range(6):
        #         img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
        #     img_color = cv2.pyrUp(cv2.pyrUp(img_color))

        #     # prepare edges
        #     img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        #     img_edges = cv2.adaptiveThreshold(
        #         cv2.medianBlur(img_edges, 7),
        #         255,
        #         cv2.ADAPTIVE_THRESH_MEAN_C,
        #         cv2.THRESH_BINARY,
        #         9,
        #         2,
        #     )
        #     img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

        #     # combine color and edges
        #     img = cv2.bitwise_and(img_color, img_edges)

        #     # rebuild a VideoFrame, preserving timing information
        #     new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        #     new_frame.pts = frame.pts
        #     new_frame.time_base = frame.time_base
        #     return new_frame
        # elif self.transform == "edges":
        #     # perform edge detection
        #     img = frame.to_ndarray(format="bgr24")
        #     img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

        #     # rebuild a VideoFrame, preserving timing information
        #     new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        #     new_frame.pts = frame.pts
        #     new_frame.time_base = frame.time_base
        #     return new_frame
        # elif self.transform == "rotate":
        #     # rotate image
        #     img = frame.to_ndarray(format="bgr24")
        #     rows, cols, _ = img.shape
        #     M = cv2.getRotationMatrix2D((cols / 2, rows / 2), frame.time * 45, 1)
        #     img = cv2.warpAffine(img, M, (cols, rows))

        #     # rebuild a VideoFrame, preserving timing information
        #     new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        #     new_frame.pts = frame.pts
        #     new_frame.time_base = frame.time_base
        #     return new_frame
        # else:
            


async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)

# async def stop_this_connection(pc):
#     transeiver = pc.getTransceivers()
#     print(pc.getSenders())
#     print(transeiver)
#     print(transeiver[0].sender)
#     print(transeiver[0].currentDirection)
#     print(transeiver[0].sender)
#     await transeiver[0].sender.send("Hello World")
#     # transeiver.send()
#     return

async def offer(request):
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
        recorder = MediaBlackhole()

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            if isinstance(message, str):
                if message.startswith("User "):
                    username = message[5:]
                    user_name[0] = username
                    channel.send("You are " + username)
                    channel.send("Passed "+ str(len(passed) > 0))


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
                track, params["video_transform"], passed, user_name
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
    ws_serve()
    app.router.add_get("/", index)
    app.router.add_get("/client.js", javascript)
    app.router.add_post("/offer", offer)
    web.run_app(app, access_log=None, port=args.port, ssl_context=ssl_context)