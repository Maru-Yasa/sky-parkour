import pygame, sys
from config import *
from level import Level
pygame.init()
pygame.mixer.init()


class Game:
	"""Summary
	
	Attributes:
	    bg (tuple): Description
	    clock (TYPE): Description
	    display (TYPE): Description
	    game_over (bool): Description
	    level (TYPE): Description
	    menu (bool): Description
	    mixer (TYPE): Description
	    ui (TYPE): Description
	"""
	def __init__(self):
		"""Summary
		"""
		self.display = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption("Infinite Sky")
		self.clock   = pygame.time.Clock()
		self.ui      = pygame.Surface((100,100))
		self.game_over = False
		self.bg = (28, 17, 23)

		self.mixer = pygame.mixer
		self.mixer.music.load('./assets/bgm.ogg')
		self.mixer.music.play(-1)

		self.setup()

	def setup(self):
		"""Summary
		"""
		self.level = Level(self.display, self.game_over_loop, self.clock)
		self.menu = True

	def event(self):
		"""Summary
		"""
		self.level.run()

	def text_header(self, text, pos, size, surface):
		"""Summary
		
		Args:
		    text (TYPE): Description
		    pos (TYPE): Description
		    size (TYPE): Description
		    surface (TYPE): Description
		"""
		font = pygame.font.Font('./assets/Symtext.ttf', size)
		text = font.render(text, True, (255,255,255))
		textRect = text.get_rect(center = pos)
		surface.blit(text,textRect)

	def text_normal(self, text, pos, size, surface):
		"""Summary
		
		Args:
		    text (TYPE): Description
		    pos (TYPE): Description
		    size (TYPE): Description
		    surface (TYPE): Description
		"""
		font = pygame.font.Font('./assets/Pixeled.ttf', size)
		text = font.render(text, True, (255,255,255))
		textRect = text.get_rect(center = pos)
		surface.blit(text,textRect)

	def menu_loop(self):
		"""Summary
		"""
		tx = int(WIDTH/2)
		ty = int(HEIGHT/2) + 50
		player_image = pygame.image.load('./assets/player.png')
		player_image = pygame.transform.scale(player_image, (64,64))
		player_image_rect = player_image.get_rect(center = (WIDTH/2,HEIGHT - 350))
		while self.menu:
			self.display.fill(self.bg)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
					pygame.QUIT
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.menu = False
				if event.type == self.level.SPWAN_PLATFORM:
					self.level.spwan_platform()

			self.text_header("Infinite Sky", (WIDTH/2,HEIGHT/4), 70, self.display)
			self.text_normal("PRESS ANYWHARE TO START", (tx,ty), 10, self.display)
			self.display.blit(player_image,player_image_rect )

			self.clock.tick(60)
			pygame.display.update()
		self.game_loop()

	def game_over_loop(self, score):
		"""Summary
		"""
		tx = int(WIDTH/2)
		ty = int(HEIGHT/2) + 50
		player_image = pygame.image.load('./assets/player.png')
		player_image = pygame.transform.scale(player_image, (64,64))
		player_image_rect = player_image.get_rect(center = (WIDTH/2,HEIGHT - 350))
		while self.menu:
			self.display.fill(self.bg)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
					pygame.QUIT
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.menu = False
				if event.type == self.level.SPWAN_PLATFORM:
					self.level.spwan_platform()

			self.text_header("GAME OVER", (WIDTH/2,HEIGHT/4), 70, self.display)
			self.text_normal("YOUR SCORE : "+str(score), (tx,ty - 50), 10, self.display)
			self.text_normal("PRESS ANYWHARE TO START", (tx,ty), 10, self.display)

			self.clock.tick(60)
			pygame.display.update()
		self.game_loop()

	def game_loop(self):
		"""Summary
		"""
		self.setup()
		while not self.game_over:
			self.display.fill(self.bg)
			self.ui.fill(self.bg)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
					pygame.QUIT
				elif event.type == self.level.SPWAN_PLATFORM:
					self.level.spwan_platform()

				elif event.type == self.level.INCREASE_SCORE:
					self.level.increase_score()
					

			self.event()
			self.clock.tick(60)
			pygame.display.update()


if __name__ == '__main__':
	game  = Game()
	game.menu_loop()
