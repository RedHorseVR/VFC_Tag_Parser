// Game constants
const WIDTH = 800;
const HEIGHT = 600;
const PADDLE_WIDTH = 20;
const PADDLE_HEIGHT = 100;
const BALL_SIZE = 15;
const PADDLE_SPEED = 8;
const INITIAL_BALL_SPEED = 7;

// Paddle class
function Paddle(x, y, width, height) {
	this.x = x;
	this.y = y;
	this.width = width;
	this.height = height;
	this.speed = PADDLE_SPEED;
}

Paddle.prototype.draw = function (ctx) {
	ctx.fillStyle = "white";
	ctx.fillRect(this.x, this.y, this.width, this.height);
};

Paddle.prototype.moveUp = function () {
	if (this.y > 0) {
		this.y -= this.speed;
	}
};

Paddle.prototype.moveDown = function () {
	if (this.y + this.height < HEIGHT) {
		this.y += this.speed;
	}
};

// Ball class
function Ball(x, y, size) {
	this.x = x;
	this.y = y;
	this.width = size;
	this.height = size;
	this.speedX = 0;
	this.speedY = 0;
	this.resetSpeed();
}

Ball.prototype.draw = function (ctx) {
	ctx.fillStyle = "white";
	ctx.beginPath();
	ctx.arc(
		this.x + this.width / 2,
		this.y + this.height / 2,
		this.width / 2,
		0,
		Math.PI * 2,
	);
	ctx.fill();
};

Ball.prototype.update = function () {
	this.x += this.speedX;
	this.y += this.speedY;

	// Top and bottom collision
	if (this.y <= 0 || this.y + this.height >= HEIGHT) {
		this.speedY *= -1;
	}
};

Ball.prototype.reset = function () {
	this.x = WIDTH / 2 - this.width / 2;
	this.y = HEIGHT / 2 - this.height / 2;
	this.resetSpeed();
};

Ball.prototype.resetSpeed = function () {
	this.speedX = INITIAL_BALL_SPEED * (Math.random() > 0.5 ? 1 : -1);
	this.speedY = INITIAL_BALL_SPEED * (Math.random() > 0.5 ? 1 : -1);
};

Ball.prototype.collidesWith = function (paddle) {
	return (
		this.x < paddle.x + paddle.width &&
		this.x + this.width > paddle.x &&
		this.y < paddle.y + paddle.height &&
		this.y + this.height > paddle.y
	);
};

// Game class
function Game() {
	this.canvas = document.getElementById("gameCanvas");
	this.ctx = this.canvas.getContext("2d");

	this.player1Score = 0;
	this.player2Score = 0;
	this.keys = {};

	// Create paddles
	this.player1 = new Paddle(
		50,
		HEIGHT / 2 - PADDLE_HEIGHT / 2,
		PADDLE_WIDTH,
		PADDLE_HEIGHT,
	);

	this.player2 = new Paddle(
		WIDTH - 50 - PADDLE_WIDTH,
		HEIGHT / 2 - PADDLE_HEIGHT / 2,
		PADDLE_WIDTH,
		PADDLE_HEIGHT,
	);

	// Create ball
	this.ball = new Ball(
		WIDTH / 2 - BALL_SIZE / 2,
		HEIGHT / 2 - BALL_SIZE / 2,
		BALL_SIZE,
	);

	// Set up event listeners
	var self = this;
	window.addEventListener("keydown", function (e) {
		self.keys[e.key] = true;
	});

	window.addEventListener("keyup", function (e) {
		self.keys[e.key] = false;
	});

	// Start game loop
	this.gameLoop();
}

Game.prototype.update = function () {
	// Player 1 controls (W & S)
	if (this.keys["w"] || this.keys["W"]) {
		this.player1.moveUp();
	}
	if (this.keys["s"] || this.keys["S"]) {
		this.player1.moveDown();
	}

	// Player 2 controls (Arrow Up & Down)
	if (this.keys["ArrowUp"]) {
		this.player2.moveUp();
	}
	if (this.keys["ArrowDown"]) {
		this.player2.moveDown();
	}

	// Update ball
	this.ball.update();

	// Ball collision with paddles
	if (
		this.ball.collidesWith(this.player1) ||
		this.ball.collidesWith(this.player2)
	) {
		this.ball.speedX *= -1;

		// Add a slight random angle for variety
		this.ball.speedY += Math.random() * 2 - 1;

		// Cap the Y speed to avoid extreme angles
		var maxYSpeed = 10;
		if (Math.abs(this.ball.speedY) > maxYSpeed) {
			this.ball.speedY = this.ball.speedY > 0 ? maxYSpeed : -maxYSpeed;
		}
	}

	// Scoring
	if (this.ball.x <= 0) {
		// Player 2 scores
		this.player2Score++;
		this.ball.reset();
	}

	if (this.ball.x + this.ball.width >= WIDTH) {
		// Player 1 scores
		this.player1Score++;
		this.ball.reset();
	}
};

Game.prototype.draw = function () {
	// Clear canvas
	this.ctx.fillStyle = "black";
	this.ctx.fillRect(0, 0, WIDTH, HEIGHT);

	// Draw center line
	this.ctx.strokeStyle = "white";
	this.ctx.setLineDash([5, 5]);
	this.ctx.beginPath();
	this.ctx.moveTo(WIDTH / 2, 0);
	this.ctx.lineTo(WIDTH / 2, HEIGHT);
	this.ctx.stroke();
	this.ctx.setLineDash([]);

	// Draw paddles and ball
	this.player1.draw(this.ctx);
	this.player2.draw(this.ctx);
	this.ball.draw(this.ctx);

	// Draw scores
	this.ctx.font = "32px Arial";
	this.ctx.fillStyle = "white";
	this.ctx.textAlign = "center";
	this.ctx.fillText(this.player1Score.toString(), WIDTH / 4, 50);
	this.ctx.fillText(this.player2Score.toString(), (3 * WIDTH) / 4, 50);
};

Game.prototype.gameLoop = function () {
	this.update();
	this.draw();

	var self = this;
	requestAnimationFrame(function () {
		self.gameLoop();
	});
};

// Start the game when DOM is loaded
window.addEventListener("DOMContentLoaded", function () {
	new Game();
});
