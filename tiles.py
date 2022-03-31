import pygame,random
from config import HEIGHT

class Tile(pygame.sprite.Sprite):
	""" class for tile """
	def __init__(self,img,wh,pos):
		super().__init__()

		self.image = pygame.image.load(img)
		self.image = pygame.transform.scale(self.image,wh)
		self.rect  = self.image.get_rect(topleft = pos)

		self.x = self.rect.x
		self.y = self.rect.y

		self.w     = wh[0]
		self.h     = wh[1]

	def move_x(self,speed):
		self.rect.x += -speed

	def move_y(self,speed):
		self.rect.y += -speed

	def die(self):
		if self.rect.y <= 0:
			self.kill()

	def update(self):
		self.die()