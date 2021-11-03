export function RTC2server(userName, isRegister) {
    // get DOM elements
    // var dataChannelLog = document.getElementById('data-channel'),
    //     iceConnectionLog = document.getElementById('ice-connection-state'),
    //     iceGatheringLog = document.getElementById('ice-gathering-state'),
    //     signalingLog = document.getElementById('signaling-state');

    // get the name of the user
    // let userName = null
    // while (true) {
    //     userName = prompt("Please enter your name", 'Jack')
    //     if (userName === null) {
    //         alert("You must input your name")
    //     } else {
    //         break;
    //     }
    // }
    console.log(userName)
    // peer connection
    var pc = null;
    start()

    function createPeerConnection() {
        var config = {
            sdpSemantics: 'unified-plan'
        };

        pc = new RTCPeerConnection(config);

        // register some listeners to help debugging
        // pc.addEventListener('icegatheringstatechange', function() {
        //     iceGatheringLog.textContent += ' -> ' + pc.iceGatheringState;
        // }, false);
        // iceGatheringLog.textContent = pc.iceGatheringState;

        // pc.addEventListener('iceconnectionstatechange', function() {
        //     iceConnectionLog.textContent += ' -> ' + pc.iceConnectionState;
        // }, false);
        // iceConnectionLog.textContent = pc.iceConnectionState;

        // pc.addEventListener('signalingstatechange', function() {
        //     signalingLog.textContent += ' -> ' + pc.signalingState;
        // }, false);
        // signalingLog.textContent = pc.signalingState;

        // connect audio / video
        pc.addEventListener('track', function(evt) {
            if (evt.track.kind == 'video')
                document.getElementById('video').srcObject = evt.streams[0];
            else
                document.getElementById('audio').srcObject = evt.streams[0];
        });

        return pc;
    }

    function negotiate() {
        return pc.createOffer().then(function(offer) {
            return pc.setLocalDescription(offer);
        }).then(function() {
            // wait for ICE gathering to complete
            return new Promise(function(resolve) {
                if (pc.iceGatheringState === 'complete') {
                    resolve();
                } else {
                    function checkState() {
                        if (pc.iceGatheringState === 'complete') {
                            pc.removeEventListener('icegatheringstatechange', checkState);
                            resolve();
                        }
                    }
                    pc.addEventListener('icegatheringstatechange', checkState);
                }
            });
        }).then(function() {
            var offer = pc.localDescription;
            // codec = 'VP8/90000'
            // document.getElementById('offer-sdp').textContent = offer.sdp;
            return fetch(isRegister? '/register': '/login', {
            // return fetch('/login', {
                body: JSON.stringify({
                    sdp: offer.sdp,
                    type: offer.type
                }),
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST'
            });
        }).then(function(response) {
            return response.json();
        }).then(function(answer) {
            // document.getElementById('answer-sdp').textContent = answer.sdp;
            return pc.setRemoteDescription(answer);
        }).catch(function(e) {
            alert(e);
        });
    }

    function start() {

        pc = createPeerConnection();

        // create data channel
        var parameters = {"ordered": true};

        let dc = pc.createDataChannel('chat', parameters);
        dc.onclose = function() {
            // clearInterval(dcInterval);
            // dataChannelLog.textContent += '- close\n';
        };
        dc.onopen = function() {
            // dataChannelLog.textContent += '- open\n';
            // dcInterval = setInterval(function() {
                // var message = userName + current_stamp();
                var message = "User " + userName;
                console.log(message)
                // dataChannelLog.textContent += '> ' + message + '\n';
                dc.send(message);
            // }, 1000);
        };
        dc.onmessage = function(evt) {
            // dataChannelLog.textContent += '< ' + evt.data + '\n';

            if (evt.data.substring(0, 7) === 'Passed ') {
                var passed = evt.data.substring(7) === 'True';
                // dataChannelLog.textContent += 'Received: ' + passed + ' \n';
                if (!passed) {
                    dc.send("check");
                } else {
                    stop();
                    dc.send('train?');
                }
            }
        };

        var constraints = {
            audio: false,
            video: true
        };

        // if (constraints.video) {
        //     document.getElementById('media').style.display = 'block';
        // }
        // var displayV = document.getElementById('video11')
        navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
            // displayV.srcObject = stream;
            stream.getTracks().forEach(function(track) {
                pc.addTrack(track, stream);
            });
            return negotiate();
        }, function(err) {
            alert('Could not acquire media: ' + err);
        });

        // document.getElementById('stop').style.display = 'inline-block';
    }

    function stop() {
        // document.getElementById('stop').style.display = 'none';

        // close transceivers
        if (pc.getTransceivers) {
            pc.getTransceivers().forEach(function(transceiver) {
                if (transceiver.stop) {
                    transceiver.stop();
                }
            });
        }

        // close local audio / video
        pc.getSenders().forEach(function(sender) {
            sender.track.stop();
        });

        // close peer connection
        setTimeout(function() {
            pc.close();
        }, 500);
    }
}


