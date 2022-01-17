import pygame
import sys
import potionParser as pp


from gui.puzzle import Puzzle

if __name__ == '__main__':
	pygame.init()
	screen_width = 800
	screen_height = 800
	screen = pygame.display.set_mode((screen_width, screen_height))
	clock = pygame.time.Clock()
	bg = pygame.Color(255, 213, 199)

	potions = pp.parse_potion_file("../res/puzzle05.txt")
	puzzle = Puzzle(screen, potions)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		screen.fill(bg)
		puzzle.display()

		pygame.display.update()
		clock.tick(60)