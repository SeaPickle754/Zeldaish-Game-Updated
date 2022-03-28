import pygame
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, QUIT
import tile
import player
import enemy
import roomLoader
import button
import bomb
import time
import math
import random
from sys import argv, exit
import bosses

class Game:
	def __init__(self, debug):
		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode((440, 510))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Legend of Ziggy: blow of the wind")
		pygame.mixer.music.load("other\\titlebytobyfox.mp3")
		pygame.mixer.music.play(-1)
		pygame.display.set_icon(pygame.image.load("other\\icon.png"))
		self.tileArray = \
			[
				[0,8,1,9,9,9,9,1,3,0,1],
				[0,0,0,0,0,8,0,0,0,0,9],
				[0,0,0,0,0,0,1,0,0,0,1],
				[0,0,0,0,2,0,0,0,0,0,1],
				[0,0,0,2,2,2,0,0,0,0,1],
				[0,0,0,2,8,2,0,1,0,0,9],
				[0,0,1,2,2,2,0,0,9,0,1],
				[0,0,0,2,2,2,0,1,0,0,9],
				[0,0,0,0,0,0,0,0,0,0,1],
				[0,1,1,1,1,1,1,1,1,0,9]
			]
		self.specialMessage = ""
		self.muted = False
		self.debug = debug
		self.tiles = []
		self.nextRoom = 2
		self.showRoomChange = False
		self.enemies = []
		self.items=[]
		self.pos = 0

		self.cutscene = False
		self.game_active = False
		self.nonPassables = ["tree", "stwl", "wate", "vtre", "notf", "corr"]
		self.exit_locked = False
		
		self.play_button = button.Button(self.screen, "Play", 200, 200)
		self.quit_button = button.Button(self.screen, "Quit", 200, 260)
		self.player = player.Player(self.screen, self.tiles)
		self.attacking = False
		self.init_tiles()
		self.enemies.append(enemy.Enemy(self.screen, self.tiles, self.player))
		self.enemies.append(enemy.Enemy(self.screen, self.tiles, self.player))
		self.bomb = None
		self.bossBar = False
		self.arrows = []
		#print(self.enemies)
		roomLoader.player = self.player
		self.mainloop()
	def plant_bomb(self):
		if not self.bomb:
			bombx = self.player.rect.x
			bomby = (self.player.rect.y + 40)
			if bombx > 0 and bombx < 440:
				if bomby > 0 and bomby < 400:
					self.bomb = bomb.Bomb(bombx, bomby, self.screen)
	def init_tiles(self):
		self.tiles = []
		for y in range(len(self.tileArray)):
			self.tiles.append([])
			for x in range(len(self.tileArray[y])):
				if self.tileArray:
					if self.tileArray[y][x] == 0:
						self.tiles[y].append(tile.Tile("tiles\\grass.png", x, y, self.screen))

					elif self.tileArray[y][x] == 1:
						self.tiles[y].append(tile.Tile("tiles\\tree.png", x, y, self.screen))

					elif self.tileArray[y][x] == 2:
						self.tiles[y].append(tile.Tile("tiles\\sand.png", x, y, self.screen))

					elif self.tileArray[y][x] == 3:
						self.tiles[y].append(tile.Tile("tiles\\tree.png", x, y, self.screen))
						self.tiles[y][x].specialType("DRCT")

					elif self.tileArray[y][x] == 4:
						self.tiles[y].append(tile.Tile("tiles\\sand.png", x, y, self.screen))
						self.tiles[y][x].specialType("DRCT")
					elif self.tileArray[y][x] == 5:
						self.tiles[y].append(tile.Tile("tiles\\stairs.png", x, y, self.screen))
						self.tiles[y][x].specialType("DRCT")
					elif self.tileArray[y][x] == 6:
						self.tiles[y].append(tile.Tile("tiles\\stone.png", x, y, self.screen))
					elif self.tileArray[y][x] == 7:
						self.tiles[y].append(tile.Tile("tiles\\stonewall.png", x, y, \
						self.screen))
					
						self.tiles[y][x].specialType("stwl")
					elif self.tileArray[y][x] == 8:
						self.tiles[y].append(tile.Tile("tiles\\water.png", x, y, \
						self.screen))
					elif self.tileArray[y][x] == 9:
						self.tiles[y].append(tile.Tile("tiles\\vtree.png", x, y, \
						self.screen))
					elif self.tileArray[y][x] == 10:
						self.tiles[y].append(tile.Tile("tiles\\back.png", x, y, \
						self.screen))
					elif self.tileArray[y][x] == 11:
						self.tiles[y].append(tile.Tile("tiles\\bwall.png", x, y, \
						self.screen))
					elif self.tileArray[y][x] == 12:
						self.tiles[y].append(tile.Tile("tiles\\corrupted.png", x, y, \
						self.screen))
					else:
						self.tiles[y].append(tile.Tile("tiles\\notfound.png", x, y, \
						self.screen))
		self.player.tiles = self.tiles


	def mainloop(self):
		self.tickspeed = 0
		self.tickspeed2 = 0
		self.tickspeed3 = 0
		self.tickspeed4 = 0
		self.tickspeed5 = 0
		self.tickspeed6 = 0
		if not self.debug:
			start_image = pygame.image.load("other\\start.png").convert()
			self.screen.blit(start_image, start_image.get_rect())
			pygame.display.flip()
			time.sleep(random.randint(1,3))
		self.update_screen()
		while(1):
			if self.player.rect.x < 0:
				self.player.rect.x = 0
			if self.player.rect.x >= 440:
				self.player.rect.x = 400
			if self.player.rect.y < 0:
				self.player.rect.y = 0
			if self.player.rect.y >= 400:
				self.player.rect.y = 360
			if self.game_active:
				self.update_tickspeed()
			if self.cutscene and not self.debug:
				time.sleep(15)
				self.cutscene = False
			self.clock.tick(60)
			self.check_events()
			self.update_screen()
	def distance(self):
		distances = []
		for e in self.enemies:
			d = (\
			int(math.sqrt(((self.player.rect.x-e.rect.x)**2) +\
				 ((self.player.rect.y-e.rect.y)**2))))
			distances.append(d)
		return distances
		
	def check_damage(self):
		distances = []
		distances = self.distance()
		for e in self.enemies:
			d = distances[self.enemies.index(e)]
			if d < 57 and type(e) != bosses.FinalBoss:
				e.health -= self.player.attack_damage
				e.image = e.dImage
				e.isDamage = True
				e.rect.x = random.randrange(0, 360, 40)
				e.rect.y = random.randrange(0, 360, 40)
				continue


	def update_tickspeed(self):
			self.tickspeed += 1
			self.tickspeed3 += 1
			self.tickspeed4 += 1
			if self.specialMessage:
				self.tickspeed6 += 1
				if self.tickspeed6 >= 200:
					self.specialMessage = ""
					self.tickspeed6 = 0
			if self.attacking:
				self.tickspeed2 += 1
				self.check_damage()
			if self.tickspeed >= 140:
				self.tickspeed = 0
				eupdate = None
				for e in self.enemies:
					if type(e) != bosses.FinalBoss and type(e) != bosses.FirstBoss:
						eupdate, self.items = e.update(self.items)
					else:
						eupdate, self.enemies, self.tileArray = e.update(self.enemies)
						self.init_tiles()
					if eupdate:
						self.enemies.remove(e)
					if e.looking_left:
						e.image = e.nimage
						e.looking_left = False
					else:
						e.image = e.limage
						e.looking_left = True
			if self.bomb:
				self.tickspeed5 += 1
			if self.tickspeed5 >= 30:
				if self.tileArray\
				[self.bomb.rect.y//40][self.bomb.rect.x//40] == 7:
					self.tileArray\
					[self.bomb.rect.y//40][self.bomb.rect.x//40] = 11

				if self.bomb.rect.y + 40 < 400:
					if self.tileArray\
					[self.bomb.rect.y//40 + 1][self.bomb.rect.x//40] == 7:
						self.tileArray\
						[self.bomb.rect.y//40 + 1][self.bomb.rect.x//40] = 11

				if not self.bomb.rect.y - 40 < 0:
					if self.tileArray\
					[self.bomb.rect.y//40 - 1][self.bomb.rect.x//40] == 7:
						self.tileArray\
						[self.bomb.rect.y//40 - 1][self.bomb.rect.x//40] = 11

				if not self.bomb.rect.x + 40 >= 440:
					if self.tileArray\
					[self.bomb.rect.y//40][self.bomb.rect.x//40 + 1] == 7:
						self.tileArray\
						[self.bomb.rect.y//40][self.bomb.rect.x//40 + 1] = 11

				if not self.bomb.rect.x - 40 < 0:
					if self.tileArray\
					[self.bomb.rect.y//40][self.bomb.rect.x//40 - 1] == 7:
						self.tileArray\
						[self.bomb.rect.y//40][self.bomb.rect.x//40 - 1] = 11

				self.tickspeed5 = 0 
				
				self.init_tiles()

				for e in self.enemies:
					if self.bomb.rect.center == e.rect.center:
						e.health -= 75
						e.image = e.dImage
						e.rect.y += 80
						e.isDamage = True
				self.bomb = None
				self.pos = pygame.mixer.music.get_pos()
				pygame.mixer.music.load("other\\explosion.wav")
				pygame.mixer.music.play()
				
			if self.tickspeed2 >= 30:
				self.player.image = self.player.nImage
				self.tickspeed2 = 0
				self.attacking = False
			if pygame.mixer.music.get_busy() and self.muted:
				pygame.mixer.music.pause()

			if self.tickspeed3 >= 10:
				self.nonPassables, self.game_active = self.player.update(\
				self.enemies, self.nonPassables, self.items, self.game_active,\
				self.muted)
				if not self.game_active:
						self.tileArray, self.items, self.exit_locked = \
						roomLoader.load(1)
						self.init_tiles()
						self.player = player.Player(self.screen, self.tiles)
						self.player.rect.x = 320
						self.player.rect.y = 200
						self.enemies = []
						roomLoader.player = self.player
						self.nextRoom = 2
						self.enemies.append(enemy.Enemy\
						(self.screen, self.tiles, self.player))
						self.pos = 0
						self.items = []
						self.tickspeed2 = 0
						self.tickspeed = 0
						self.tickspeed3 = 0
						self.tickspeed4 = 0
						self.tickspeed5 = 0
						self.tickspeed6 = 0
						return

				if not pygame.mixer.music.get_busy()\
				and self.nextRoom == 18 and len(self.enemies)\
				 and self.game_active and not self.muted:
					pygame.mixer.music.load("other\\BossMusicMetriodPrime.mp3")
					pygame.mixer.music.play(-1)
					pygame.mixer.music.set_pos(self.pos/1000)
					self.pos = 0

				if not pygame.mixer.music.get_busy() and self.game_active \
					and not self.muted:
					pygame.mixer.music.load("other\\backgroundbytobyfox.mp3")
					pygame.mixer.music.play(-1)
					pygame.mixer.music.set_pos(self.pos/1000)

				if not pygame.mixer.music.get_busy() and self.game_active == False\
					and not self.muted:
					pygame.mixer.music.load("other\\titlebytobyfox.mp3")
					pygame.mixer.music.play(-1)

				if self.nextRoom == 13 and not len(self.enemies)\
				 and self.exit_locked == True and not self.muted:
					pygame.mixer.music.load("other\\itempickup.wav")
					pygame.mixer.music.play(1)
					self.exit_locked = False

				if self.nextRoom == 13 and not len(self.enemies)\
				 and self.exit_locked == True and self.muted:
					self.exit_locked = False

				if self.nextRoom == 18 and not len(self.enemies)\
				 and self.exit_locked == True and not self.muted:
					pygame.mixer.music.load("other\\itempickup.wav")
					pygame.mixer.music.play(1)
					self.exit_locked = False

				if self.nextRoom == 18 and not len(self.enemies)\
				and self.exit_locked == True and self.muted:
					self.exit_locked = False

					for e in self.enemies:
						if type(e) == bosses.FinalBoss:
							self.bossBar = True

			if self.tickspeed4 % 100 == 0:
				for e in self.enemies:
					if e.isDamage:
						e.isDamage = False
						e.image = e.nimage
			for e in self.enemies:
				if e.rect.x < 0:
					e.rect.x += 40
				if e.rect.x >= 400:
					e.rect.x -= 40
				if e.rect.y < 0:
					e.rect.y += 40
				if e.rect.y >= 400:
					e.rect.y -= 40

				if self.tickspeed4 == 100000:	self.tickspeed4 = 0
	def draw_text(self):
		font = pygame.font.Font("other\\ARCADECLASSIC.TTF", 10)
			
		img = font.render(f'Your  Health   {self.player.health}', True, (0, 255, 0))
		self.screen.blit(img, (2, 400))

		img = font.render(f'Current  Room   {self.nextRoom-1}', True, (0, 255, 0))
		self.screen.blit(img, (2, 422))

		try:
			ehealth = self.enemies[0].health
			if ehealth < 0:
				ehealth = 0
		except IndexError:
			ehealth = 0
		img= font.render(f'Enemy   {ehealth}', True, (0, 255, 0))
		self.screen.blit(img, (100, 400))
		if self.player.hasSnorkel:
			img= font.render(f'Swimming   {self.player.canSwim}', True, (0, 255, 0))
			self.screen.blit(img, (130, 422)) 	
		if self.player.hasBombs:
			img= font.render(f'Bombs    {self.player.bombs}', True, (0, 255, 
			0))
			self.screen.blit(img, (220, 400))
		if self.debug:
			img= font.render(f'DTE   {self.distance()}', True, (0, 255, 
			0))
			self.screen.blit(img, (220, 422))
			img= font.render(f'FPS   {self.clock.get_fps()}', True, (0, 255, 
			0))
			self.screen.blit(img, (220, 480))
		if self.specialMessage:
			img= font.render(self.specialMessage, True, (0, 255, 
			0))
			self.screen.blit(img, (2, 450))
		
	def update_screen(self):
		pygame.Surface.unlock(self.screen)
		self.screen.fill((0, 0, 0))
		for t in self.tiles:
			for t2 in t:
				if t2.type == "DRCT" and self.showRoomChange:
					pygame.draw.rect(self.screen, (255, 0, 0), t2.rect)
					continue
				t2.draw()
		if self.bossBar:
			try:
				pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(20, 490, self.enemies[0].health // 2, 500))
			except:
				self.bossBar = False
		for i in self.items:
			i.draw(self.screen)
		for e in self.enemies:
			e.draw()
		self.player.draw()
		if not self.game_active:
			self.play_button.draw_button()
			self.quit_button.draw_button()
		if self.bomb:
			self.bomb.draw()
		self.draw_text()
		pygame.Surface.lock(self.screen)
		pygame.display.flip()

	def check_roomChange(self):
		if self.player.current_tile == "DRCT" and not self.exit_locked:
			self.tileArray, self.items, self.exit_locked = \
			roomLoader.load(self.nextRoom)
			self.init_tiles()
			self.nextRoom += 1
			self.showRoomChange = False  
			self.enemies = []
			self.enemies.append(enemy.Enemy\
				(self.screen, self.tiles, self.player))
			self.enemies.append(enemy.Enemy(self.screen, self.tiles, self.player))
			self.showRoomChange = False
			self.specialMessage = "room changed!"
			if self.nextRoom == 13:
				self.enemies = []
				self.enemies.append(bosses.FirstBoss(self.screen, self.tiles, self.player, self.tileArray))
				pygame.mixer.music.load("other\\BossMusicByTobyFox.mp3")
				pygame.mixer.music.play(-1)
			if self.nextRoom == 18:
				self.enemies = []
				self.enemies.append(bosses.FinalBoss(self.screen, self.tiles, self.player, self.tileArray))
				pygame.mixer.music.load("other\\BossMusicMetriodPrime.mp3")
				pygame.mixer.music.play(-1)
				self.cutscene = True
	def check_back(self):
		if self.player.current_tile == "back":
			self.nextRoom -= 1
			self.tileArray, self.items, self.exit_locked = \
			roomLoader.load(self.nextRoom - 1)
			self.init_tiles()
			self.showRoomChange = False
			self.enemies = []
			self.enemies.append(\
			enemy.Enemy(self.screen, self.tiles, self.player))
			self.enemies.append(enemy.Enemy(self.screen, self.tiles, self.player))
	def check_events(self):
		pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN and self.game_active:
				if event.key == pygame.K_LEFT:
					if self.player.rect.x > 0:
						self.player.rect.x -= 40
						self.player.get_current_tile()
						if self.player.current_tile in self.nonPassables:
							self.player.rect.x += 40
							self.player.get_current_tile()
						self.check_roomChange()
						self.check_back()

				if event.key == pygame.K_RIGHT:
					if self.player.rect.x < 400:
						self.player.rect.x += 40
						self.player.get_current_tile()
						if self.player.current_tile in self.nonPassables:
							self.player.rect.x -= 40
							self.player.get_current_tile()
						
						self.check_roomChange()
						self.check_back()

				if event.key == pygame.K_UP:
					if self.player.rect.y > 0:
						self.player.rect.y -= 40
						self.player.get_current_tile()
						if self.player.current_tile in self.nonPassables:
							self.player.rect.y += 40
							self.player.get_current_tile()
						self.check_roomChange()
						self.check_back()

				if event.key == pygame.K_DOWN:
					if self.player.rect.y < 360:
						self.player.rect.y += 40
						self.player.get_current_tile()
						if self.player.current_tile in self.nonPassables:
							self.player.rect.y -= 40
							self.player.get_current_tile()
						
						self.check_roomChange()
						self.check_back()
				if event.key == pygame.K_SPACE:
					self.attacking = True
					self.player.image = self.player.attacking_image

				if event.key == pygame.K_s and self.player.hasSnorkel:
					self.player.canSwim = not self.player.canSwim

				if event.key == pygame.K_b and self.player.hasBombs and\
				self.player.bombs > 0:
					self.plant_bomb()
					self.player.bombs -= 1

				if event.key == pygame.K_p:
					self.game_active = False
					self.specialMessage = "paused"
					self.pos = pygame.mixer.music.get_pos()
					pygame.mixer.music.stop()
					return

				if event.key == pygame.K_c:
					self.showRoomChange = not self.showRoomChange
					self.specialMessage = "showing room change"

				if event.key == pygame.K_m:
					if self.muted:
						pygame.mixer.music.unpause()
						self.muted = False
						return

					self.muted = not self.muted
					pygame.mixer.music.pause()
				
				if self.debug:
					if event.key == pygame.K_i:
						self.specialMessage = "Reloading!"
						self.init_tiles()

			if event.type == pygame.KEYDOWN and not self.game_active:
				if event.key == pygame.K_m:
					if self.muted:
						pygame.mixer.music.unpause()
						self.muted = False
						return
					self.muted = not self.muted
					pygame.mixer.music.pause()
				if event.key == pygame.K_p:
					self.game_active = not self.game_active
					pygame.mixer.music.stop()


			if event.type == pygame.MOUSEBUTTONDOWN and not self.game_active:
				if self.play_button._check_button(pygame.mouse.get_pos()):
					self.game_active = True

					pygame.mixer.music.stop()
				if self.quit_button._check_button(pygame.mouse.get_pos()):
					exit()
try:
	if len(argv) == 2:
		if argv[1] == "-d" or argv[1] == "--debug":
			game = Game(True)
	else:
		game = Game(False)
except KeyboardInterrupt:
	print("program ended from keyboard")
	exit()