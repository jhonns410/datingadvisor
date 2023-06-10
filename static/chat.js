function openChat() {
    document.getElementById("chatPopup").style.display = "block";
}

function closeChat() {
    document.getElementById("chatPopup").style.display = "none";
}

function sendMessage(event) {
    event.preventDefault();
    var userMessageInput = document.getElementById("userMessageInput");
    var chatContent = document.getElementById("chatContent");

    var userMessage = document.createElement("p");
    userMessage.textContent = userMessageInput.value;
    chatContent.appendChild(userMessage);

    // Send user message to the server and receive the response
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessageInput.value })
    })
    .then(response => response.json())
    .then(data => {
        var response = document.createElement("p");
        response.textContent = data.response;
        chatContent.appendChild(response);
    })
    .catch(error => {
        console.error('Error:', error);
    });

    userMessageInput.value = "";
}
