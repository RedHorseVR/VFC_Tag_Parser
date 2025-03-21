// Game constants
const WIDTH: number = 800;
const HEIGHT: number = 600;
const PADDLE_WIDTH: number = 20;
const PADDLE_HEIGHT: number = 100;
const BALL_SIZE: number = 15;
const PADDLE_SPEED: number = 8;
const INITIAL_BALL_SPEED: number = 7;

// Game objects interfaces
interface GameObject {
    x: number;
    y: number;
    width: number;
    height: number;
    draw(ctx: CanvasRenderingContext2D): void;
}

class Paddle implements GameObject {
    x: number;
    y: number;
    width: number;
    height: number;
    speed: number;
    
    constructor(x: number, y: number, width: number, height: number) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.speed = PADDLE_SPEED;
    }
    
    draw(ctx: CanvasRenderingContext2D): void {
        ctx.fillStyle = "white";
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
    
    moveUp(): void {
        if (this.y > 0) {
            this.y -= this.speed;
        }
    }
    
    moveDown(): void {
        if (this.y + this.height < HEIGHT) {
            this.y += this.speed;
        }
    }
}

class Ball implements GameObject {
    x: number;
    y: number;
    width: number;
    height: number;
    speedX: number = 0; // Initialize with default value
    speedY: number = 0; // Initialize with default value
    
    constructor(x: number, y: number, size: number) {
        this.x = x;
        this.y = y;
        this.width = size;
        this.height = size;
        this.resetSpeed();
    }
    
    draw(ctx: CanvasRenderingContext2D): void {
        ctx.fillStyle = "white";
        ctx.beginPath();
        ctx.arc(
            this.x + this.width / 2, 
            this.y + this.height / 2, 
            this.width / 2, 
            0, 
            Math.PI * 2
        );
        ctx.fill();
    }
    
    update(): void {
        this.x += this.speedX;
        this.y += this.speedY;
        
        // Top and bottom collision
        if (this.y <= 0 || this.y + this.height >= HEIGHT) {
            this.speedY *= -1;
        }
    }
    
    reset(): void {
        this.x = WIDTH / 2 - this.width / 2;
        this.y = HEIGHT / 2 - this.height / 2;
        this.resetSpeed();
    }
    
    resetSpeed(): void {
        this.speedX = INITIAL_BALL_SPEED * (Math.random() > 0.5 ? 1 : -1);
        this.speedY = INITIAL_BALL_SPEED * (Math.random() > 0.5 ? 1 : -1);
    }
    
    collidesWith(paddle: Paddle): boolean {
        return (
            this.x < paddle.x + paddle.width &&
            this.x + this.width > paddle.x &&
            this.y < paddle.y + paddle.height &&
            this.y + this.height > paddle.y
        );
    }
}

class Game {
    canvas: HTMLCanvasElement;
    ctx: CanvasRenderingContext2D;
    player1: Paddle;
    player2: Paddle;
    ball: Ball;
    player1Score: number = 0;
    player2Score: number = 0;
    keys: { [key: string]: boolean } = {};
    
    constructor() {
        this.canvas = document.getElementById("gameCanvas") as HTMLCanvasElement;
        this.ctx = this.canvas.getContext("2d") as CanvasRenderingContext2D;
        
        // Create paddles
        this.player1 = new Paddle(
            50, 
            HEIGHT / 2 - PADDLE_HEIGHT / 2, 
            PADDLE_WIDTH, 
            PADDLE_HEIGHT
        );
        
        this.player2 = new Paddle(
            WIDTH - 50 - PADDLE_WIDTH, 
            HEIGHT / 2 - PADDLE_HEIGHT / 2, 
            PADDLE_WIDTH, 
            PADDLE_HEIGHT
        );
        
        // Create ball
        this.ball = new Ball(
            WIDTH / 2 - BALL_SIZE / 2, 
            HEIGHT / 2 - BALL_SIZE / 2, 
            BALL_SIZE
        );
        
        // Set up event listeners
        window.addEventListener("keydown", (e) => {
            this.keys[e.key] = true;
        });
        
        window.addEventListener("keyup", (e) => {
            this.keys[e.key] = false;
        });
        
        // Start game loop
        this.gameLoop();
    }
    
    update(): void {
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
        if (this.ball.collidesWith(this.player1) || this.ball.collidesWith(this.player2)) {
            this.ball.speedX *= -1;
            
            // Add a slight random angle for variety
            this.ball.speedY += (Math.random() * 2 - 1);
            
            // Cap the Y speed to avoid extreme angles
            const maxYSpeed = 10;
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
    }
    
    draw(): void {
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
        this.ctx.fillText(this.player2Score.toString(), 3 * WIDTH / 4, 50);
    }
    
    gameLoop(): void {
        this.update();
        this.draw();
        requestAnimationFrame(() => this.gameLoop());
    }
}

// Start the game when DOM is loaded
window.addEventListener("DOMContentLoaded", () => {
    new Game();
});