import sys, time
from PyGM.master import *
import math
from random import choice, randrange

pygame.display.init()

pygame.font.init()
mono_font = pygame.font.SysFont("monospace", 12)

screen = pygame.display.set_mode((640, 480))
FPS = 15
clock = pygame.time.Clock()

# Rectanlge Coords
ROOM = (64, 64)
HALL = (32, 16)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

running = True
pygame.display.set_caption("Dungeon Generator")

color_list = [RED, WHITE, GREEN, BLUE]

class GameTimer(Entity):
	def __init__(self, **kw):
		super(GameTimer, self).__init__(**kw)

	def event_step(self):
		super(GameTimer, self).event_step()

class Room(Entity):
	def __init__(self, **kw):
		super(Room, self).__init__(**kw)

	def draw(self):
		draw_rect(screen, WHITE, self, ROOM)

class Hall(Entity):
	def __init__(self, **kw):
		super(Hall, self).__init__(**kw)

	def draw(self):
		draw_rect(screen, WHITE, self, HALL)

size = 16

NewGameRoom()
NewGameRoom.add_object(0, 0, GameTimer)
NewGameRoom.add_object(128, 128, Room)

start_room = NewGameRoom.object_index(1)

struct_list = ["room", "hall"]
room_list = []

def generate(cellsX, cellsY, cellSize=72):

	class Cell(object):
		def __init__(self, x, y, id, type, drawn):
			self.x = x
			self.y = y 
			self.id = id
			self.type = type
			self.drawn = drawn

	cells = {}
	last_x = 0
	last_y = 0

	max_steps = 15

	for y in range (cellsY):
		for x in range(cellsX):
			cell_id = len(cells) + 1
			c = Cell(x, y, cell_id, None, False)
			cells[((c.x * cellSize), (c.y * cellSize), c.id, None, False)] = c

	for i in cells:
		direction = randrange(1, 5)
		choice = randrange(1, 6)
		x = i[0]
		y = i[1]
		id = i[2]
		type = i[3]
		drawn = i[4]
		cell = cells[(x, y, id, type, drawn)]
		if choice == 2:
			pygame.draw.rect(screen, RED, (x, y, cellSize, cellSize))
			cell.drawn = True
			num = mono_font.render(str(id), 1, BLUE)
			screen.blit(num, (x, y))
			last_x = x
			last_y = y
		elif last_x == x:
			last_x = x
			pygame.draw.rect(screen, RED, (x, y, cellSize, cellSize))
			num = mono_font.render(str(id), 1, BLUE)
			screen.blit(num, (x, y))
		elif last_y == y:
			last_y = y
			pygame.draw.rect(screen, RED, (x, y, cellSize, cellSize))
			num = mono_font.render(str(id), 1, BLUE)
			screen.blit(num, (x, y))
		else:
			pass


generate(20, 15, 32)

while running:
	keys = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (keys[pygame.K_ESCAPE]):
			running = False

	#start_room.draw()

	NewGameRoom.room_step()
	clock.tick(FPS)

	pygame.display.flip()