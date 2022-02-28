from random import randrange
import pygame

import enemy

class Player:

	def __init__(self, screen, tiles):
		self.nImage = pygame.image.load("other\\player.png").convert_alpha()
		self.attacking_image = pygame.image.load("other\\player_attacking.png").convert_alpha()
		self.image = self.nImage
		self.rect = self.image.get_rect()
		self.screen = screen
		self.rect.x = 320
		self.rect.y = 200
		self.hasBombs = False
		self.bombs = 0
		self.attack_damage = 3
		self.health = 5
		self.tiles = tiles
		self.canSwim = False
		self.hasSnorkel = False
		self.hasMachete = False
		#self.current_tile = self.tiles[self.rect.y//40][self.rect.x//40].type
	def get_current_tile(self):
		self.current_tile = self.tiles[self.rect.y//40][self.rect.x//40].type
		#print(self.current_tile)
	def update(self, enemies, nonPassables, items, game_active, isMuted):
		for e in enemies:
			if e.rect.x - self.rect.x == 0 and e.rect.y - self.rect.y == 0:
				e.rect.y = 0
				e.rect.x = randrange(0, 400, 40)
				e.rect.y = randrange(0, 360, 40)
				self.health -= 1

			if self.rect.x < 0:
				self.rect.x = 0
			if self.rect.x >= 440:
				self.rect.x = 400
			if self.rect.y < 0:
				self.rect.y = 0
			if self.rect.y >= 400:
				self.rect.y = 360
			if self.health <= 0:
				pygame.mixer.music.stop()
				game_active = False
		if self.canSwim\
		and "gras" not in nonPassables:
			nonPassables = ["tree","gras", "stwl", "sand", "ston"]
		if not self.canSwim and "gras" in nonPassables:
			nonPassables = ["tree", "stwl", "wate"]
		if self.hasMachete and "vtre" in nonPassables:
			nonPassables.remove("vtre")

		for i in items:
			if i.x == self.rect.x and\
			i.y == self.rect.y:
				items.remove(i)
				i.onPlayerCollision(isMuted)
		return nonPassables, game_active
	def draw(self):
		self.screen.blit(self.image, self.rect)
