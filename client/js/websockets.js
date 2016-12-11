var ws = new WebSocket("ws://" + window.location.hostname + ":80/server/")
var snakes = snakes || {};
var identity = null
ws.onmessage = function (event) {
    // content = document.createTextNode(event.data);
    // console.log(content)
    message = JSON.parse(event.data)
    console.log(message)
    switch (message.type) {
        case "greeting": {
            identity = message.id
            break;
        }
        case "initial": {
            snakes = {}
            for (var k in message.info) {
                if (message.info.hasOwnProperty(k)) {
                    snakes[k] = new Snake(k, new Position(message.info[k].head.x, message.info[k].head.y), message.info[k].length, message.info[k].direction)
                }
            }
            console.log(snakes)
            break;
        }
        case "partial": {
            for (var k in message.live_info) {
                if (message.live_info.hasOwnProperty(k) && snakes.hasOwnProperty(k)) {
                    snakes[k].update(new Position(message.live_info[k].head.x, message.live_info[k].head.y), message.live_info[k].direction)
                }
            }
            break;
        }
        case "winner": {
            if (identity == message.id) {
                ShowMessage('You are the Winner!!!!');
            } else {
                ShowMessage('Loser!');
            }
            break;
        }
        case "draw": {
            ShowMessage('Draw');
            break;
        }
        case "busy": {

        }
        default: {
            console.log(message.type)
            break;
        }
    }

};

