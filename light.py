import pygame

class Light(pygame.sprite.Sprite):
	def __init__(self,img,wh,pos):
		super().__init__()
		self.image = pygame.image.load(img)
		self.image = pygame.transform.scale(self.image,wh)
		self.rect = self.image.get_rect(center = pos)

	def update(self,x,y):
		self.rect.x += x
		self.rect.y += y