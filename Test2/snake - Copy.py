

import pygame
import time
import random
import math
pygame.init()
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
GAME_DURATION = 120
class Particle:
	
	
	
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color
		self.size = random.randint(2, 5)
		self.speed_x = random.uniform(-3, 3)
		self.speed_y = random.uniform(-3, 3)
		self.lifetime = random.randint(20, 30)
		
	def update(self):
		self.x += self.speed_x
		self.y += self.speed_y
		self.lifetime -= 1
		
	def draw(self, surface):
		pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
		
	def is_dead(self):
		return self.lifetime <= 0
		
		
def show_score(score):
	font = pygame.font.SysFont("times new roman", 20)
	score_surface = font.render(f"Score : {score}", True, WHITE)
	screen.blit(score_surface, (10, 10))
	
def show_speed(speed):
	font = pygame.font.SysFont("times new roman", 20)
	speed_surface = font.render(f"Speed : {speed} FPS", True, WHITE)
	screen.blit(speed_surface, (WIDTH - 150, 10))
	
def show_timer(time_left):
	font = pygame.font.SysFont("times new roman", 20)
	color = RED if time_left < 30 else YELLOW if time_left < 60 else WHITE
	time_surface = font.render(f"Time : {time_left} sec", True, color)
	screen.blit(time_surface, (WIDTH // 2 - 50, 10))
	
def game_over(score, time_expired=False):
	screen.fill(BLACK)
	font = pygame.font.SysFont("times new roman", 50)
	if time_expired:
	
		go_surface = font.render("TIME'S UP!", True, YELLOW)
		
	else:
		go_surface = font.render("GAME OVER", True, RED)
		
	screen.blit(go_surface, (WIDTH // 4, HEIGHT // 3 - 50))
	score_font = pygame.font.SysFont("times new roman", 36)
	score_surface = score_font.render(f"Final Score: {score}", True, WHITE)
	screen.blit(score_surface, (WIDTH // 4, HEIGHT // 2))
	pygame.display.flip()
	time.sleep(3)
	pygame.quit()
	quit()
	
def create_explosion(x, y, num_particles=30):
	particles = []
	colors = [RED, ORANGE, YELLOW, WHITE]
	for _ in range(num_particles):
		color = random.choice(colors)
		particles.append(Particle(x + BLOCK_SIZE / 2, y + BLOCK_SIZE / 2, color))
		
	
	return particles

def get_snake_color(score):
	if score < 20:
	
		return GREEN
		
	elif score < 50:
		return BLUE
		
	elif score < 100:
		return PURPLE
		
	elif score < 150:
		return CYAN
		
	else:
		colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
		return colors[int(pygame.time.get_ticks() / 200) % len(colors)]
		
	
def game_loop():
	snake_pos = [100, 50]
	snake_body = [[100, 50], [90, 50], [80, 50]]
	direction = "RIGHT"
	change_to = direction
	food_pos = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE, random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
	food_spawn = True
	score = 0
	game_speed = 15
	particles = []
	start_time = pygame.time.get_ticks()
	time_left = GAME_DURATION
	while True:
		current_time = pygame.time.get_ticks()
		elapsed_seconds = (current_time - start_time) // 1000
		time_left = max(0, GAME_DURATION - elapsed_seconds)
		if time_left == 0:
		
			game_over(score, time_expired=True)
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
			
				pygame.quit()
				quit()
				
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
						
					
				elif event.key == pygame.K_1:
					game_speed = max(5, game_speed - 2)
					
				elif event.key == pygame.K_2:
					game_speed = min(30, game_speed + 2)
					
				
			
		
		direction = change_to
		if direction == "UP":
		
			snake_pos[1] -= BLOCK_SIZE
			
		if direction == "DOWN":
		
			snake_pos[1] += BLOCK_SIZE
			
		if direction == "LEFT":
		
			snake_pos[0] -= BLOCK_SIZE
			
		if direction == "RIGHT":
		
			snake_pos[0] += BLOCK_SIZE
			
		if snake_pos[0] < 0:
		
			snake_pos[0] = WIDTH - BLOCK_SIZE
			
		if snake_pos[0] >= WIDTH:
		
			snake_pos[0] = 0
			
		if snake_pos[1] < 0:
		
			snake_pos[1] = HEIGHT - BLOCK_SIZE
			
		if snake_pos[1] >= HEIGHT:
		
			snake_pos[1] = 0
			
		snake_body.insert(0, list(snake_pos))
		if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
		
			score += 10
			food_spawn = False
			particles = create_explosion(food_pos[0], food_pos[1])
			
		else:
			snake_body.pop()
			
		if not food_spawn:
		
			food_pos = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE, random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
			
		food_spawn = True
		screen.fill(BLACK)
		for particle in particles[:]:
			particle.update()
			if particle.is_dead():
			
				particles.remove(particle)
				
			else:
				particle.draw(screen)
				
			
		
		snake_color = get_snake_color(score)
		for i, block in enumerate(snake_body):
			if i == 0:
			
				pygame.draw.rect(screen, snake_color, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
				
			else:
				darkness = min(i * 10, 100)
				adjusted_color = tuple(max(c - darkness, 0) for c in snake_color)
				pygame.draw.rect(screen, adjusted_color, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
				
			
		
		pygame.draw.rect(screen, WHITE, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
		for block in snake_body[1:]:
			if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
			
				game_over(score)
				
			
		
		show_score(score)
		show_speed(game_speed)
		show_timer(time_left)
		pygame.display.update()
		clock.tick(game_speed)
		
	
	
if __name__ == "__main__":

	game_loop()
	

#  Export  Date: 02:36:09 PM - 24:Mar:2025.

