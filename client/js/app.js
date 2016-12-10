
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
canvas.width = 50 * pxPerBox;
canvas.height = 50 * pxPerBox;
document.body.appendChild(canvas);

var snakes = [
    {
        id: 1,
        direction: 2,
        boxes: [
            [10, 20],
            [9, 20],
            [8, 20],
            [7, 20],
            [6, 20],
            [5, 20],
            [4, 20],
            [3, 20],
            [2, 20],
            [1, 20]
        ]
    },
    {
        id: 2,
        direction: 4,
        boxes: [
            [32,30],
            [33,30],
            [34,30],
            [35,30],
            [36,30],
            [37,30],
            [38,30],
            [39,30],
            [40,30],
            [41,30]
        ]
    }
];


// The main game loop
var lastTime;
function main() {
    var now = Date.now();
    var dt = (now - lastTime) / 1000.0;

    update(dt);
    render();

    lastTime = now;
    console.log(lastTime);
    requestAnimFrame(main);
};
init();
function init() {
    main();
}

// Update game objects
function update(dt) {
    handleInput();
};

function handleInput() {
    if(input.isDown('DOWN') || input.isDown('s')) {
        alert(1)
    }

    if(input.isDown('UP') || input.isDown('w')) {
        alert(1)
    }

    if(input.isDown('LEFT') || input.isDown('a')) {
        alert(1)
    }

    if(input.isDown('RIGHT') || input.isDown('d')) {
        alert(1)
    }
}

// Draw everything
function render()  {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    snakes.forEach(function(snake) {
        renderSnake(snake);
        popped = snake.boxes.pop();
        popped[0]++;
        popped[1]++;
        snake.boxes.unshift(popped);
    });
};

function renderSnake(snake) {
    snake.boxes.forEach(function(box) {
       renderBox(box[0], box[1]);
    });
}

function renderBox(x, y) {
    ctx.rect(x*pxPerBox, y*pxPerBox, pxPerBox, pxPerBox);
    var dotMargin = pxPerBox / 3;
    ctx.fillStyle="white";
    ctx.fillRect(x*pxPerBox + dotMargin, y*pxPerBox + dotMargin, pxPerBox - dotMargin*2, pxPerBox - dotMargin*2);
    ctx.lineWidth=1;
    ctx.strokeStyle="white";
    ctx.stroke();
}