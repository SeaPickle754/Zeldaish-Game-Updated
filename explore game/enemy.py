import pygame
import random
import item
class Enemy:

	def __init__(self, screen, tiles, player):
		self.nimage = pygame.image.load("other\\enemy.png").convert_alpha()
		self.limage = pygame.image.load("other\\lenemy.png").convert_alpha()
		self.image = self.nimage
		random.seed(random.randint(0, 100000))
		self.rect = self.image.get_rect()
		self.screen = screen
		self.playerobj = player
		self.looking_left = False
		self.player = player.rect
		self.dImage = pygame.image.load("other\\dEnemy.png").convert_alpha()
		self.rect.x = random.randrange(0, 360, 40)
		self.heath = 5
		# the ai type of the enemy
		# 0 = normal
		# 1 = 'noob' (random movement)
		# 2 = 'tryhard' (little bit more health)
		# 3 = 'evade'
		self.type = random.randint(0, 30)
		self.rect.y = random.randrange(0, 360, 40)
		self.tiles = tiles
		self.health = 5
		if self.type > 20:
				self.health = 7
		self.isDamage = False
		if self.playerobj.hasBombs:
			self.drop = random.randint(1, 2)
		else:
			self.drop = 1
		self.current_tile = self.tiles[self.rect.y//40][self.rect.x//40].type
	def get_current_tile(self):
		self.current_tile = self.tiles[self.rect.y//40][self.rect.x//40].type
		#print(self.current_tile)
	def update(self, items):
		if self.type <= 10 or self.type > 20:
			if self.player.x < self.rect.x:
				self.rect.x -= 40
			if self.player.x > self.rect.x:
				self.rect.x += 40
			if self.player.y < self.rect.y:
				self.rect.y -= 40
			if self.player.y > self.rect.y:
				self.rect.y += 40
		if self.type >= 10 and self.type <= 20:
			direction = random.randint(0, 3)
			if direction == 0:
				self.rect.x += 40
			if direction == 1:
				self.rect.x -= 40
			if direction == 2:
				self.rect.y += 40
			if direction == 3:
				self.rect.y -= 40
		if self.health <= 0:
			if self.drop == 1:
				items.append(item.Item("items\\medpack.png", self.rect.x, \
				self.rect.y, 5, self.playerobj))
			else:
				items.append(item.Item("items\\bombrefill.png", self.rect.x, \
				self.rect.y, 6, self.playerobj))
			return 1,items 
		else:
			return 0, items
	def draw(self):
		self.screen.blit(self.image, self.rect)
