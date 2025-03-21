import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
PADDLE_SPEED = 8
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()

# Font for score
font = pygame.font.SysFont("Arial", 32)

# Game objects
player1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(
    WIDTH - 50 - PADDLE_WIDTH,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)
ball = pygame.Rect(
    WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE
)

# Game variables
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))
player1_score = 0
player2_score = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player controls
    keys = pygame.key.get_pressed()

    # Player 1 (left paddle)
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += PADDLE_SPEED

    # Player 2 (right paddle)
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += PADDLE_SPEED

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1
        # Add a slight random angle to make gameplay more interesting
        ball_speed_y += random.uniform(-1, 1)
        # Keep speed within reasonable bounds
        if abs(ball_speed_y) > 10:
            ball_speed_y = 10 if ball_speed_y > 0 else -10

    # Ball out of bounds - scoring
    if ball.left <= 0:
        # Player 2 scores
        player2_score += 1
        # Reset ball
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
        ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

    if ball.right >= WIDTH:
        # Player 1 scores
        player1_score += 1
        # Reset ball
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
        ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

    # Drawing
    screen.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw center line
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw scores
    player1_text = font.render(str(player1_score), True, WHITE)
    player2_text = font.render(str(player2_score), True, WHITE)
    screen.blit(player1_text, (WIDTH // 4, 20))
    screen.blit(player2_text, (3 * WIDTH // 4, 20))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)
