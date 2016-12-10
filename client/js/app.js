Math.random() //uncache feature
// A cross-browser requestAnimationFrame
// See https://hacks.mozilla.org/2011/08/animating-with-javascript-from-setinterval-to-requestanimationframe/
var requestAnimFrame = (function(){
    return function(callback){
            window.setTimeout(callback, 1000 / 1);
        };

        window.requestAnimationFrame       ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame    ||
        window.oRequestAnimationFrame      ||
        window.msRequestAnimationFrame     ||
        function(callback){
            window.setTimeout(callback, 1000 / 60);
        };
})();

// Create the canvas
var canvas = document.createElement("canvas");
var ctx = canvas.getContext("2d");
var pxPerBox = 10;
canvas.width = 130 * pxPerBox;
canvas.height = 70 * pxPerBox;
document.body.appendChild(canvas);


var Position = function(x, y) {
    this.x = x;
    this.y = y;
};

var Snake = function(id, headPosition, length, direction) {
    var renderPosition = function(position) {
        setPositionRect(position)
        var dotMargin = pxPerBox / 3;
        ctx.rect(position.x*pxPerBox, position.y*pxPerBox, pxPerBox, pxPerBox);
        ctx.fillStyle = "white"
        ctx.fillRect(position.x*pxPerBox + dotMargin, position.y*pxPerBox + dotMargin, pxPerBox - dotMargin*2, pxPerBox - dotMargin*2);
//        ctx.lineWidth = 2
//        ctx.strokeStyle = "white"
//        ctx.stroke();
    }

    var setPositionRect = function(position) {
        return
    }
    this.body = [headPosition];
    for(i = 1; i < length; i++) {
        lastX = this.body[i - 1].x;
        lastY = this.body[i - 1].y;
        nextPosition = new Position(lastX - getXFactor(direction) , lastY - getYFactor(direction));
        this.body.push(nextPosition);
        renderPosition(nextPosition)
    }
    this.direction = direction;
    this.id = id;
    this.update = function(headPosition, direction) {
        console.log("id:", this.id, "headPosition", headPosition)
        this.body.unshift(headPosition)

        tail = this.body.pop()
//        ctx.clearRect(tail.x*pxPerBox, tail.y*pxPerBox, pxPerBox, pxPerBox)
//        ctx.lineWidth = 0
//        ctx.strokeStyle = "black"
//        ctx.stroke();
        this.body.forEach(function(position) {
            renderPosition(position)
        })
    }




};

var snakes = [
    new Snake("1", new Position(90, 20), 10, 3),
    new Snake("2", new Position(30, 40), 10, 1)
];

main();
// The main game loop
var lastTime;
function main() {
    handle();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#444444';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    snakes.forEach(function(snake) {
        headPosition = getActualHeadPosition(snake)
        direction = getActualDirection(snake)
        snake.update(headPosition, direction)
    })

    requestAnimFrame(main);
};

function getActualDirection(snake) {
    return snake.direction
}

function getActualHeadPosition(snake) {
    return new Position(snake.body[0].x + getXFactor(snake.direction), snake.body[0].y + getYFactor(snake.direction))
}

function handle() {
    if(input.isDown('DOWN')) {
        ws.send(3)
    }

    if(input.isDown('UP')) {
        ws.send(0)
    }

    if(input.isDown('LEFT')) {
        ws.send(1)
    }

    if(input.isDown('RIGHT')) {
        ws.send(2)
    }
}


function getXFactor(direction) {
    if(direction === 1) {
        return -1
    }
    if(direction === 3) {
        return 1
    }
    return 0
}

function getYFactor(direction) {
    if(direction === 0) {
        return -1
    }
    if(direction === 2) {
        return 1
    }
    return 0
}