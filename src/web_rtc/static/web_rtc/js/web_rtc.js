'use strict';


let remoteRTCMessage;
let peerConnection;
let dataChannel;

let remoteStream;
let localStream = new MediaStream();
let localVideo = document.querySelector('#localVideo');
let remoteVideo = document.querySelector('#remoteVideo');

let callInProgress = false;

let otherUser = {
    name: '',
    avatar: ''
};

const constraints = {
    video: true,
    audio: false
};

let pcConfig = {
    iceServers: [
        {urls: 'stun:stun.jap.bloggernepal.com:5349'},
        {
            urls: "turn:178.250.157.153:3478",
            username: "test",
            credential: "test123"
        }
    ],
};


function login(blogUserName, blogUserId) {
    console.log(blogUserId);
    let userName;
    if (!blogUserName) {
        userName = document.getElementById("userNameInput").value;
    } else
    userName = blogUserName
    user.name = userName;
    document.getElementById("userName").style.display = "none";
    document.getElementById("call").style.display = "block";
    document.getElementById("userNameText").innerHTML = userName;

    connectSocket();
}

//user html events
function call() {
    otherUser.name = document.getElementById("calleeName").value;;

    beReady()
        .then(bool => {
            processCall(otherUser.name)
        })
}

function declineCall() {
    callSocket.send(JSON.stringify({
        type: 'declineCall',
        data: {
            user: otherUser.name
        }
    }));
    stop();
}

function answer() {
    //do the event firing
    beReady()
        .then(bool => {
            processAccept();
        })
    document.getElementById("answer").style.display = "none";
}


function beReady() {
    return navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
            localStream = stream;
            localVideo.srcObject = stream;

            return createConnectionAndAddStream()
        })
        .catch(function (e) {
            alert('getUserMedia() error: ' + e.name);
        });
}



let callSocket;
function connectSocket() {
    let ws_scheme = "ws://";
    console.log(ws_scheme);

    callSocket = new WebSocket(
        ws_scheme
        + window.location.host
        + '/ws/call/'
    );

    callSocket.onopen = event =>{
        callSocket.send(JSON.stringify({
            type: 'login',
            data: {
                name: user.name
            }
        }));
    }

    callSocket.onmessage = (e) =>{
        let response = JSON.parse(e.data);
        let type = response.type;


        switch (type) {
            case "connection":
                console.log(response.data.message)
                break;
            case "offer":
                console.log("call_received");
                onOfferCall(response.data)
                console.log('offer')
                break;
            case "answer":
                console.log("call_answered");
                onCallAnswer(response.data);
                break;
            case "candidate":
                onICECandidate(response.data);
                console.log('candidate')
                break;
            case "declineCall":
                console.log('declineCall')
                stop();
                break;
            default:
                break;
        }
    }

    const onOfferCall = (data) =>{
        //when other called you
        //show answer button
        callInProgress = true;
        otherUser.name = data.caller;

        console.log('offer setRemoteRTCMessage rtc message', data.rtcMessage)
        remoteRTCMessage = data.rtcMessage

        if (data.avatar) {
            otherUser.avatar = data.avatar;
            document.getElementById("callerNameAvatar").src = data.avatar;
        }
        document.getElementById("callerNameText").innerHTML = otherUser.name;
        document.getElementById("call").style.display = "none";
        document.getElementById("answer").style.display = "block";
    }

    const onCallAnswer = (data) =>{
        //when other accept our call
        remoteRTCMessage = data.rtcMessage
        console.log('answer setRemoteDescription onCallAnswered', remoteRTCMessage)
        peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));

        document.getElementById("calling").style.display = "none";

        callProgress()
    }

    const onICECandidate = (data) =>{
        let message = data.rtcMessage

        let candidate = new RTCIceCandidate({
            sdpMLineIndex: message.label,
            candidate: message.candidate
        });

        if (peerConnection) {
            peerConnection.addIceCandidate(candidate);
        }
    }

}


function sendCall(data) {
    callSocket.send(JSON.stringify({
        type: 'offer',
        data
    }));

    document.getElementById("call").style.display = "none";
    document.getElementById("calleeNameText").innerHTML = otherUser.name;
    document.getElementById("calling").style.display = "block";
}



function answerCall(data) {
    callSocket.send(JSON.stringify({
        type: 'answer',
        data
    }));
    callProgress();
}


function sendICEcandidate(data) {
    callSocket.send(JSON.stringify({
        type: 'candidate',
        data
    }));
}



function createConnectionAndAddStream() {
    createPeerConnection();
    peerConnection.addStream(localStream);
    return true;
}

function processCall(otherUserName) {
    callInProgress = true;
    peerConnection.createOffer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);
        sendCall({
            name: otherUserName,
            avatar: user.avatar,
            rtcMessage: sessionDescription
        })
    }, (error) => {
        console.log("Error");
    });
}

function processAccept() {
    peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage)).then(() => {
        console.log('setRemoteDescription processAccept', remoteRTCMessage)
        return peerConnection.createAnswer();
    }).then((answer) => {
        console.log('Answer create');
        console.log('setRemoteDescription processAccept', answer)
        peerConnection.setLocalDescription(answer)

        answerCall({
            caller: otherUser.name,
            rtcMessage: answer
        })
    });
}



function createPeerConnection() {
    try {
        peerConnection = new RTCPeerConnection(pcConfig);
        peerConnection.onicecandidate = handleIceCandidate;
        peerConnection.onaddstream = handleRemoteStreamAdded;
        peerConnection.onremovestream = handleRemoteStreamRemoved;

        dataChannel = peerConnection.createDataChannel("dataChannel", {
            reliable: true
        })

        dataChannel.onerror = function (error) {
            console.log("Error occured on datachannel:", error)
        }

        dataChannel.onmessage = function (event) {
            console.log("message:", event.data)
        }

        dataChannel.onclose = function () {
            stop();
        }

        peerConnection.ondatachannel = function (event) {
            dataChannel = event.channel
        }
    } catch (e) {
        alert('Cannot create RTCPeerConnection object.');
    }
}

function handleIceCandidate(event) {
    //send only if we have caller, else no need to
    if (event.candidate) {
        sendICEcandidate({
            user: otherUser.name,
            rtcMessage: {
                label: event.candidate.sdpMLineIndex,
                id: event.candidate.sdpMid,
                candidate: event.candidate.candidate
            }
        })

    } else {
        console.log('End of candidates.');
    }
}

function handleRemoteStreamAdded(event) {
    remoteStream = event.stream;
    remoteVideo.srcObject = remoteStream;
}

function handleRemoteStreamRemoved(event) {
    remoteVideo.srcObject = null;
    localVideo.srcObject = null;
}

window.onbeforeunload = function () {
    if (callInProgress) {
        declineCall();
    }
};


// close peerConnection
function stop() {
    localStream.getTracks().forEach(track => track.stop());
    callInProgress = false;
    if (peerConnection) {
        peerConnection.close();
    }
    peerConnection = null;
    document.getElementById("call").style.display = "block";
    document.getElementById("answer").style.display = "none";
    document.getElementById("inCall").style.display = "none";
    document.getElementById("calling").style.display = "none";
    document.getElementById("videos").style.display = "none";
    otherUser = { name: '', avatar: '' }
}

// display call
function callProgress() {
    document.getElementById("videos").style.display = "block";
    document.getElementById("otherUserNameCall").innerHTML = otherUser.name;
    document.getElementById("inCall").style.display = "block";

    callInProgress = true;
}


