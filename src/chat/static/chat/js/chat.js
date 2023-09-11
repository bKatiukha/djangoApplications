messagesBlock = document.getElementById("messages")
messageInput = document.getElementById("message-input")
messageInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      send_message(user.name)
    }
});

let chatSocket;
function connectSocket(uuid) {
    messagesBlock.scrollTo(0, messagesBlock.scrollHeight);
    let ws_scheme = "ws://";
    console.log(ws_scheme);

    chatSocket = new WebSocket(
        ws_scheme
        + window.location.host
        + `/ws/chat/${uuid}`
    );

    chatSocket.onmessage = (e) => {
        let response = JSON.parse(e.data);
        let type = response.type;


        switch (type) {
            case "connection":
                console.log(response.data.message)
                break;
            case "chat_message":
                console.log("chat_message");
                displayChatMessage(response.data)
                break;
        }
    }
}

function displayChatMessage(data) {
    newMessage = `<div class="message-row"><div>
                        ${data.created_by}: ${data.message}
                    </div></div>`
    messagesBlock.innerHTML += newMessage
    messagesBlock.scrollTo(0, messagesBlock.scrollHeight);
}

function send_message(userName) {
    if (messageInput.value) {
        chatSocket.send(JSON.stringify({
            type: 'chat_message',
            data: {
                created_by: userName,
                message: messageInput.value
            }
        }));
        messageInput.value = '';
    }
}


function copyToClipboard(uuid) {
    window.location.href.toString()
    navigator.clipboard.writeText(window.location.href.toString()+ uuid);
}

function goToChat(uuid) {
    window.location.href = window.location.href.toString() + uuid;
}