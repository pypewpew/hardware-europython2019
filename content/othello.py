import pew
import array
try:
	import random
except ImportError:
	import urandom as random

def lookup(board, x, y):
	return 0 if x < 0 or y < 0 or x >= 8 or y >= 8 else board[y*8 + x]

def move(board, x, y, color):
	if lookup(board, x, y) != 0:
		return None
	turned = False
	newboard = bytearray(board)
	newboard[8*y + x] = color
	for dx, dy in ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)):
		nx = x
		ny = y
		while True:
			nx += dx
			ny += dy
			v = lookup(board, nx, ny)
			if v == 0:
				break
			elif v == color:
				while True:
					nx -= dx
					ny -= dy
					if nx == x and ny == y:
						break
					newboard[8*ny + nx] = color
					turned = True
				break
	return newboard if turned else None

def count(board):
	weight = (3, 1, 2, 1, 1, 2, 1, 3)
	c = bytearray(3)
	for y in range(8):
		for x in range(8):
			c[board[y*8+x]] += weight[x]*weight[y]
	return c[2]/(c[1]+c[2])

def evaluate(board, color, depth):
	max = -1.0
	maxx = -1
	maxy = -1
	for y in range(8):
		for x in range(8):
			newboard = move(board, x, y, color)
			if newboard:
				if depth == 0:
					c = count(newboard)
					if color == 1:
						c = 1.0 - c
				else:
					othermax = evaluate(newboard, color^3, depth - 1)[0]
					if othermax != -1.0:
						c = 1.0 - othermax
					else:
						c = count(newboard)
						if color == 1:
							c = 1.0 - c
				if c > max or (c == max and random.getrandbits(1) == 0):
					max = c
					maxx = x
					maxy = y
	return max, maxx, maxy

keyhistory = 0
def keyevents():
	global keyhistory
	keys = pew.keys()
	events = keys & (~keyhistory | (keyhistory & (keyhistory >> 8) & (keyhistory >> 16)))
	keyhistory = ((keyhistory & 0xFFFF) << 8) | keys
	return events

pew.init()
screen = pew.Pix()
board = bytearray(64)
board[27] = 1
board[28] = 2
board[35] = 2
board[36] = 1
cursorx = 1
cursory = 1

blink = 0
error = 0
turn = 1
difficulty = 2 #0..2
while True:
	if turn == 2:
		#pew.tock()
		_, x, y = evaluate(board, turn, difficulty)
		if x >= 0 and y >= 0:
			board = move(board, x, y, turn)
		turn = 1
	
	keys = keyevents()
	if keys & pew.K_O:
		newboard = move(board, cursorx, cursory, turn)
		if newboard:
			board = newboard
			turn = turn ^ 3
		else:
			error = 4
	if keys & pew.K_X:
		turn = turn ^ 3
	if keys & pew.K_RIGHT:
		cursorx = (cursorx + 1) & 7
		error = 0
	if keys & pew.K_LEFT:
		cursorx = (cursorx - 1) & 7
		error = 0
	if keys & pew.K_UP:
		cursory = (cursory - 1) & 7
		error = 0
	if keys & pew.K_DOWN:
		cursory = (cursory + 1) & 7
		error = 0
	blink = 0 if keys != 0 else (blink + 1) % 6
	
	screen.blit(pew.Pix(8, 8, board))
	if blink < 2 and turn == 1:
		screen.pixel(cursorx, cursory, turn if lookup(board, cursorx, cursory) == 0 and error == 0 else 3)
	if error != 0:
		error -= 1
	pew.show(screen)
	pew.tick(0.06)
