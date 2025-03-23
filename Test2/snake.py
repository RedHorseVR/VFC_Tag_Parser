

import pygame
import time
import random
pygame.init()
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = "RIGHT"
change_to = direction
food_pos = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE, random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
food_spawn = True
score = 0
def show_score(choice, color, font, size):
	font = pygame.font.SysFont(font, size)
	score_surface = font.render(f"Score : {score}", True, color)
	screen.blit(score_surface, (10, 10))
	
def game_over():
	font = pygame.font.SysFont("times new roman", 50)
	go_surface = font.render("GAME OVER", True, RED)
	screen.blit(go_surface, (WIDTH // 4, HEIGHT // 3))
	pygame.display.flip()
	time.sleep(2)
	pygame.quit()
	quit()
	
while True:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
		
			if event.key == pygame.K_UP:
			
				if direction != "DOWN":
				
					change_to = "UP"
					
				
			elif event.key == pygame.K_DOWN:
				if direction != "UP":
				
					change_to = "DOWN"
					
				
			elif event.key == pygame.K_LEFT:
				if direction != "RIGHT":
				
					change_to = "LEFT"
					
				
			elif event.key == pygame.K_RIGHT:
				if direction != "LEFT":
				
					change_to = "RIGHT"
					
				
			
		
	
	direction = change_to
	if direction == "UP":
	
		snake_pos[1] -= BLOCK_SIZE
		
	if direction == "DOWN":
	
		snake_pos[1] += BLOCK_SIZE
		
	if direction == "LEFT":
	
		snake_pos[0] -= BLOCK_SIZE
		
	if direction == "RIGHT":
	
		snake_pos[0] += BLOCK_SIZE
		
	snake_body.insert(0, list(snake_pos))
	if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
	
		score += 10
		food_spawn = False
		
	else:
		snake_body.pop()
		
	if not food_spawn:
	
		food_pos = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE, random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
		
	food_spawn = True
	screen.fill(BLACK)
	for block in snake_body:
		pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
		
	
	pygame.draw.rect(screen, WHITE, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
	if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
	
		game_over()
		
	for block in snake_body[1:]:
		if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
		
			game_over()
			
		
	
	show_score(1, WHITE, "times new roman", 20)
	pygame.display.update()
	clock.tick(15)
	


#  Export  Date: 10:20:43 PM - 22:Mar:2025.

