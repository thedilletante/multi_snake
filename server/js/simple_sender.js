ws = new WebSocket("ws://127.0.0.1:5678/"),
    messages = document.createElement('ul');
ws.onmessage = function (event) {
    var messages = document.getElementsByTagName('ul')[0],
        message = document.createElement('li'),
        content = document.createTextNode(event.data);
    message.appendChild(content);
    messages.appendChild(message);
};
document.body.appendChild(messages);

function my_left() {
    ws.send('{"direction":"LEFT"}')
};

function my_up() {
    ws.send('{"direction":"TOP"}')
};

function my_bottom() {
    ws.send('{"direction":"BOTTOM"}')
};

function my_right() {
    ws.send('{"direction":"RIGHT"}')
};
