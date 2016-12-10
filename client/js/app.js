Math.random() //uncache feature
// A cross-browser requestAnimationFrame
// See https://hacks.mozilla.org/2011/08/animating-with-javascript-from-setinterval-to-requestanimationframe/
var requestAnimFrame = (function(){
    return window.requestAnimationFrame       ||
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
canvas.width = 140 * pxPerBox;
canvas.height = 75 * pxPerBox;
document.body.appendChild(canvas);
ctx.fillStyle = '#000000';
ctx.fillRect(0, 0, canvas.width, canvas.height);

var Position = function(x, y) {
    this.x = x;
    this.y = y;
};

var Snake = function(id, headPosition, length, direction) {
    this.body = [headPosition];
    console.log(this.body);
    for(i = 1; i < length; i++) {
        console.log(this.body.length);
        lastX = this.body[i - 1].x;
        lastY = this.body[i - 1].y;
        console.log("coordinates:", lastX, lastY);
        nextPosition = new Position(lastX - getXFactor(direction) , lastY - getYFactor(direction));
        console.log("new position", nextPosition)
        this.body.push(nextPosition);
    }
    this.direction = direction;
    this.id = id;
};

var snakes = [
    new Snake("1", new Position(10, 20), 10, 3),
    new Snake("1", new Position(32, 30), 10, 1)
];
render(snakes)

main();
// The main game loop
var lastTime;
function main() {
    handle();
    requestAnimFrame(main);
};

function handle() {
    if(input.isDown('DOWN')) {
            alert(1)
    }

    if(input.isDown('UP')) {
        alert(1)
    }

    if(input.isDown('LEFT')) {
        alert(1)
    }

    if(input.isDown('RIGHT')) {
        alert(1)
    }
}



// Draw everything
function render(snakes)  {
    snakes.forEach(function(snake) {
        renderSnake(snake);
    });
};

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

function renderSnake(snake) {
//    console.log(snake)
    snake.body.forEach(function(position) {
//        console.log(position)
       renderPosition(position);
    });
}

function renderPosition(position) {
    ctx.rect(position.x*pxPerBox, position.y*pxPerBox, pxPerBox, pxPerBox);
    var dotMargin = pxPerBox / 3;
    ctx.fillStyle="white";
    ctx.fillRect(position.x*pxPerBox + dotMargin, position.y*pxPerBox + dotMargin, pxPerBox - dotMargin*2, pxPerBox - dotMargin*2);
    ctx.lineWidth=1;
    ctx.strokeStyle="white";
    ctx.stroke();
}

function hideBox(box) {
}