let onlineUsersBlock = document.querySelector('#online_users');

onlineUsersSocket.onmessage = (e) =>{
    console.log('response')
    let response = JSON.parse(e.data);
    let type = response.type;

    console.log('response', response)
    switch (type) {
        case "connection":
            console.log(response.data.message)
            break;
        case "online_users":
            displayOnlineUsers(response.data['online_users'])
            break;
        case "user_left":
            removeUser(response.data['username'])
            break;
        case "user_in":
            displayUser(response.data['user'])
            break;
    }
}

function displayOnlineUsers(users) {
    for (const user of users) {
        displayUser(user)
    }
}

function displayUser(user) {
    const userBlock = document.createElement("div");
    userBlock.id = user.username;
    userBlock.className = "online-user";

    const avatar = document.createElement("img");
    avatar.src = user.avatar;
    const username = document.createElement("div");
    username.textContent = user.username[0];

    userBlock.appendChild(avatar);
    userBlock.appendChild(username);

    onlineUsersBlock.appendChild(userBlock)
}

function removeUser(username) {
    console.log('remove user')
    console.log(username);
    console.log(`[id="${username}"]`)
    console.log(document.querySelector(`[id="${username}"]`));
    document.querySelector(`[id="${username}"]`).remove()
}