import pygame
import numpy as np
pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
DARKGREEN = (0,122,0)
# BLUE = (0,0,255)

size = (750, 500)
screen = pygame.display.set_mode(size)
while True:
	pygame.draw.line(screen, WHITE, [10, 30], [10, 470], 5) # y axis
	pygame.draw.line(screen, WHITE, [10, 470], [700, 470], 5) # x axis
	s = 50 # number of sections
	l = 15 # length (mm) of sections
	first = 235 # initial 
	# for f_region in range(first, first+(s*l)): # frequency ranges
	# 	pygame.draw.line(screen, DARKGREEN, [10, f_region], [f_region+l, first], 3)
	pygame.draw.line(screen, DARKGREEN, [13, 235], [10+15, first], 5)
	pygame.display.flip()