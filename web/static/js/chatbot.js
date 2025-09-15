document.getElementById("chat-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        let message = this.value;
        this.value = "";

        let chatMessages = document.getElementById("chat-messages");
        chatMessages.innerHTML += "<div><b>Tú:</b> " + message + "</div>";

        fetch(`/chat/ask/?message=${encodeURIComponent(message)}`)
            .then(res => res.json())
            .then(data => {
                chatMessages.innerHTML += "<div><b>Bot:</b> " + data.respuesta + "</div>";
                chatMessages.scrollTop = chatMessages.scrollHeight;
            });
    }
});