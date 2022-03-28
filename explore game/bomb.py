import pygame

class Bomb:
	def __init__(self, x, y, screen):
		self.image = pygame.image.load("items\\bomb.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.screen = screen
	def draw(self):
		self.screen.blit(self.image, self.rect)
