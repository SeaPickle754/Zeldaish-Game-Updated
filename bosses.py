import pygame
from random import randint, seed, randrange
from enemy import Enemy
from tile import Tile
class FinalBoss:

	def __init__(self, screen, tiles, player, tileArray):
		self.nimage = pygame.image.load("other\\finalBoss.png").convert_alpha()
		self.limage = pygame.image.load("other\\finalBoss.png").convert_alpha()
		self.image = self.nimage
		self.rect = self.image.get_rect()
		self.screen = screen
		self.tileArray = tileArray
		self.playerobj = player
		self.looking_left = False
		seed()
		self.tiles = tiles
		self.player = player.rect
		self.dImage = pygame.image.load("other\\finalBoss.png").convert_alpha()
		self.health = 750
		self.isDamage = False
	def update(self, enemies):
		if self.player.x < self.rect.x:
			self.rect.x -= 40
		if self.player.x > self.rect.x:
			self.rect.x += 40
		if self.player.y < self.rect.y:
			self.rect.y -= 40
		if self.player.y > self.rect.y:
			self.rect.y += 40
		if self.isDamage:
			self.rect.x = randrange(0, 400, 40)
			self.rect.y = randrange(0, 360, 40)
		attack = randint(0, 10)
		if attack < 6 and attack > 3:
			enemies.append(Enemy(self.screen, self.tiles, self.playerobj))
		if attack > 5:
			self.tileArray[self.rect.y//40][self.rect.x//40] = 12
		if attack < 4:
			self.rect.x = randrange(0, 400, 40)
			self.rect.y = randrange(0, 360, 40)
		if self.health <= 0:
			return True, enemies, self.tileArray
		return False, enemies, self.tileArray
        
	def draw(self):
		self.screen.blit(self.image, self.rect)

class FirstBoss:
	def __init__(self, screen, tiles, player, tileArray):
		self.nimage = pygame.image.load("other\\enemy.png").convert_alpha()
		self.limage = pygame.image.load("other\\lenemy.png").convert_alpha()
		self.image = self.nimage
		self.rect = self.image.get_rect()
		self.screen = screen
		self.tileArray = tileArray
		self.playerobj = player
		self.looking_left = False
		seed()
		self.tiles = tiles
		self.player = player.rect
		self.dImage = pygame.image.load("other\\denemy.png").convert_alpha()
		self.health = 100
		self.isDamage = False
	def update(self, enemies):
		if self.player.x < self.rect.x:
			self.rect.x -= 40
		if self.player.x > self.rect.x:
			self.rect.x += 40
		if self.player.y < self.rect.y:
			self.rect.y -= 40
		if self.player.y > self.rect.y:
			self.rect.y += 40
		if self.isDamage:
			self.rect.x = randrange(0, 400, 40)
			self.rect.y = randrange(0, 360, 40)
		if randint(0, 10) < 5:
			if self.tiles[self.rect.x // 40][self.rect.y // 40].type == "DRCT":
				self.tileArray[self.rect.x // 40][self.rect.y // 40] = 7
			if self.player.rect.x // 40 == self.rect.y // 40:
				if self.player.rect.y // 40 == self.rect.x // 40:
					self.player.x = self.player.x - 40
					self.player.y = self.player.y - 40
					self.playerobj.health -= 1
		if self.health <= 0:
			return True, enemies, self.tileArray
		return False, enemies, self.tileArray
		


        
	def draw(self):
		self.screen.blit(self.image, self.rect)