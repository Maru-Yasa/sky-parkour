import pygame
from config import HEIGHT

class Player(pygame.sprite.Sprite):
	"""class for player"""
	def __init__(self,img,wh,pos):
		super().__init__()
		self.image = pygame.image.load(img)
		self.image = pygame.transform.scale(self.image,wh)
		self.image_normal = self.image
		self.image_flipped = pygame.transform.flip(self.image,True,False)
		self.image = self.image_normal

		self.rect  = self.image.get_rect(topleft = pos)
		self.w     = wh[0]
		self.h     = wh[1]

		self.speed = 5
		self.gravity = 0.2
		self.jump_speed = -12
		self.direction = pygame.math.Vector2(0,0)
		self.life = 5

		self.on_ground = True
		self.flipped   = False
		self.is_die    = False
		self.is_fall   = False

	def jump(self):
		self.on_ground = False
		self.direction.y = self.jump_speed

	def input(self):
		keys = pygame.key.get_pressed()
		events = pygame.event.get()

		if keys[pygame.K_a]:
			# left
			self.rect.x += -self.speed
			self.flipped = True

		elif keys[pygame.K_d]:
			# right
			self.rect.x += self.speed
			self.flipped = False

		elif keys[pygame.K_a] and keys[pygame.K_w]:
			# left and jump
			self.rect.x += -self.speed
			self.jump()
			self.flipped = True

		elif keys[pygame.K_d] and keys[pygame.K_w]:
			# right and jump
			self.rect.x += self.speed
			self.jump
			self.flipped = False

		elif keys[pygame.K_w] and self.on_ground:
			self.jump()

		else:
			self.rect.x += 0
			self.rect.y += 0 

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def check_fall(self):
		if self.rect.y > HEIGHT:
			return True

	def animate(self):
		if self.flipped:
			self.image = self.image_flipped
		else:
			self.image = self.image_normal

	def die(self):
		if self.rect.y > HEIGHT and self.life >= 0:
			self.life -= 1
			self.is_fall = True
		elif self.rect.y > HEIGHT and self.life <= 0:
			self.is_die = True
			self.is_fall = True

	def move(self,pos):
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.is_fall = False

	def update(self):
		self.input()
		self.apply_gravity()
		self.animate()
		self.die()
