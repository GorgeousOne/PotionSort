import pygame
from gui.flask import Flask
from typing import List

from potion import Potion


class Puzzle:

	def __init__(self, surface:pygame.Surface, potions: List[Potion]):
		self.display_surface = surface
		self.flasks = self.create_flasks(potions)

	def create_flasks(self, potions: List[Potion]) -> pygame.sprite.Group:
		group = pygame.sprite.Group()
		for i, p in enumerate(potions):
			group.add(Flask((100 + i * 100, 100), p))
		return group

	def display(self):
		self.flasks.draw(self.display_surface)
