var ws = new WebSocket("ws://localhost:5678/")
ws.onmessage = function (event) {
    content = document.createTextNode(event.data);
    alert(content)
};

