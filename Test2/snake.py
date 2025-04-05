

import pygame
import random
import time
pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
class Snake:
	
	
	
	def __init__(self):
		self.positions = [(WIDTH // 2, HEIGHT // 2)]
		self.direction = 'RIGHT'
		self.length = 1
		self.score = 0
		
	def move(self):
		head_x, head_y = self.positions[0]
		if self.direction == 'UP':
		
			new_head = (head_x, head_y - BLOCK_SIZE)
			
		elif self.direction == 'DOWN':
			new_head = (head_x, head_y + BLOCK_SIZE)
			
		elif self.direction == 'LEFT':
			new_head = (head_x - BLOCK_SIZE, head_y)
			
		elif self.direction == 'RIGHT':
			new_head = (head_x + BLOCK_SIZE, head_y)
			
		self.positions.insert(0, new_head)
		if len(self.positions) > self.length:
		
			self.positions.pop()
			
		
	def change_direction(self, new_direction):
		if (new_direction == 'UP' and self.direction != 'DOWN') or (new_direction == 'DOWN' and self.direction != 'UP') or (new_direction == 'LEFT' and self.direction != 'RIGHT') or (new_direction == 'RIGHT' and self.direction != 'LEFT'):
		
			self.direction = new_direction
			
		
	def check_collision(self):
		head_x, head_y = self.positions[0]
		if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
		
			return True
			
		for pos in self.positions[1:]:
			if pos == self.positions[0]:
			
				return True
				
			
		
		return False
		
	def grow(self):
		self.length += 1
		self.score += 10
		
	def draw(self, surface):
		for i, (x, y) in enumerate(self.positions):
			color = GREEN if i == 0 else (0, 200, 0)
			pygame.draw.rect(surface, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
			pygame.draw.rect(surface, (0, 100, 0), (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)
			
		
		
		
class Food:
	
	
	
	def __init__(self):
		self.position = self.generate_position()
		
	def generate_position(self):
		x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
		y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
		return (x, y)
		
	def draw(self, surface):
		pygame.draw.rect(surface, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))
		
	def respawn(self, snake_positions):
		while True:
			new_pos = self.generate_position()
			if new_pos not in snake_positions:
			
				self.position = new_pos
				break
				
			
		
		
		
def draw_score(surface, score):
	font = pygame.font.SysFont('Arial', 25)
	score_text = font.render(f'Score: {score}', True, WHITE)
	surface.blit(score_text, (10, 10))
	
def game_over_screen(surface, score):
	surface.fill(BLACK)
	font_large = pygame.font.SysFont('Arial', 50)
	font_small = pygame.font.SysFont('Arial', 30)
	game_over_text = font_large.render('Game Over!', True, RED)
	score_text = font_small.render(f'Your Score: {score}', True, WHITE)
	restart_text = font_small.render('Press R to Restart or Q to Quit', True, WHITE)
	surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
	surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))
	surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2 + 50))
	pygame.display.update()
	
def main():
	running = True
	game_active = True
	snake = Snake()
	food = Food()
	fps = 10
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
			
				running = False
				
			if event.type == pygame.KEYDOWN:
			
				if game_active:
				
					if event.key == pygame.K_UP:
					
						snake.change_direction('UP')
						
					elif event.key == pygame.K_DOWN:
						snake.change_direction('DOWN')
						
					elif event.key == pygame.K_LEFT:
						snake.change_direction('LEFT')
						
					elif event.key == pygame.K_RIGHT:
						snake.change_direction('RIGHT')
						
					
				else:
					if event.key == pygame.K_r:
					
						snake = Snake()
						food = Food()
						game_active = True
						
					elif event.key == pygame.K_q:
						running = False
						
					
				
			
		
		if game_active:
		
			snake.move()
			if snake.check_collision():
			
				game_active = False
				
			if snake.positions[0] == food.position:
			
				snake.grow()
				food.respawn(snake.positions)
				if snake.score % 50 == 0:
				
					fps += 1
					
				
			screen.fill(BLACK)
			snake.draw(screen)
			food.draw(screen)
			draw_score(screen, snake.score)
			pygame.display.update()
			
		else:
			game_over_screen(screen, snake.score)
			
		clock.tick(fps)
		
	
	pygame.quit()
	
if __name__ == "__main__":

	main()
	

#  Export  Date: 02:44:54 PM - 03:Apr:2025.

