import math

import pygame
from pygame import gfxdraw

class Flask(pygame.sprite.Sprite):

	def __init__(self, pos, potion):
		super().__init__()
		self.image = pygame.Surface((50, 150))
		self.image.fill("white")
		self.rect = self.image.get_rect(topleft=pos)
		self.draw_shape("black")

	def draw_shape(self, c):
		mid_x = self.image.get_width() / 2
		mid_y = self.image.get_height() / 2
		print(mid_x, mid_y)
		stroke = 3
		w = 20
		h = 60

		pygame.draw.rect(self.image, c, (mid_x - w, mid_y - h, 2*w, 2*h), width=stroke)
	# def display(self):
	# 	pass