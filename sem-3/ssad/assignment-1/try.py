#!/usr/bin/env python
# -*- coding: utf-8 -*-

import msvcrt, os, time, sys, random, math

random.seed()

columns = 15		#\
									# adjustable, odd numbers only
lines = 15			#/  

score = 0
pPos = 0				#top left corner starting position

explosions = range(10,16)
bombs = range(20,33)

spf = 0.25			#seconds per frame
bombPower = 2
maxBombs = 1
activeBombs = []
activeExplosions = []
brokenBoxes = [] 
activeBombCount = 0
percentBoxes = 0.6			# percent of screen filled with destructible boxes

# 0 = AIR, 1 = BLOCK, 2 = DESTRUCTIBLE_BLOCK, 3 = PLAYER_BOMB, 4 = PLAYER,
# 5 = POWERUP_BOMB_STRENGTH, 6 = POWERUP_BOMB_AMOUNT, 10-15 = EXPLOSION, 20-32 = BOMB

def InitArray():
	global gameArray
	
	gameArray = [0] * (lines*columns)
	
	for i in range(lines):
		for j in range(columns):
			if (i == 0 and j == 0):
				gameArray[i * columns + j] = 4
			elif (i == 1 and j == 0) or (i == 0 and j == 1):
				gameArray[i * columns + j] = 0
			elif i % 2 and j % 2:
				gameArray[i * columns + j] = 1
			elif random.random() < percentBoxes:
				gameArray[i * columns + j] = 2
				
			
				
				
def Render():
	os.system('cls')
	
	print('+'),
	for column in range(columns):
		print('-'),
	print('+')
	
	for line in range(lines):
	
		print("|"),
		
		for column in range(columns):
		

			if gameArray[(line * columns) + column] == 0: 			# AIR
				print(" "),
			elif gameArray[(line * columns) + column] == 1: 		# BLOCK
				print("X"),
			elif gameArray[(line * columns) + column] == 2:			# DESTRUCTIBLE_BLOCK
				print("#"),
			elif gameArray[(line * columns) + column] == 3:			# PLAYER_BOMB
				print("p"),
			elif gameArray[(line * columns) + column] == 4:			# PLAYER
				print("P"),
			elif gameArray[(line * columns) + column] == 5:			# POWERUP_BOMB_POWER
				print("S"),
			elif gameArray[(line * columns) + column] == 6:			# POWERUP_BOMB_AMOUNT
				print("A"),
			elif gameArray[(line * columns) + column] == 10:		# EXPLOSION
				print("@"),
			elif gameArray[(line * columns) + column] == 11:		# EXPLOSION
				print("a"),
			elif gameArray[(line * columns) + column] == 12:		# EXPLOSION
				print("@"),
			elif gameArray[(line * columns) + column] == 13:		# EXPLOSION
				print("a"),
			elif gameArray[(line * columns) + column] == 14:		# EXPLOSION
				print("@"),
			elif gameArray[(line * columns) + column] == 15:		# EXPLOSION
				print("a"),
			elif gameArray[(line * columns) + column] == 20:			# BOMB
				print("o"),
			elif gameArray[(line * columns) + column] == 21:			# BOMB
				print("o"),
			elif gameArray[(line * columns) + column] == 22:			# BOMB
				print("O"),
			elif gameArray[(line * columns) + column] == 23:			# BOMB
				print("O"),
			elif gameArray[(line * columns) + column] == 24:			# BOMB
				print("o"),
			elif gameArray[(line * columns) + column] == 25:			# BOMB
				print("o"),
			elif gameArray[(line * columns) + column] == 26:			# BOMB
				print("O"),
			elif gameArray[(line * columns) + column] == 27:			# BOMB
				print("O"),
			elif gameArray[(line * columns) + column] == 28:			# BOMB
				print("o"),
			elif gameArray[(line * columns) + column] == 29:			# BOMB
				print("o"),
			elif gameArray[(line * columns) + column] == 30:			# BOMB
				print("o"),
			elif gameArray[(line * columns) + column] == 31:			# BOMB
				print("O"),
			elif gameArray[(line * columns) + column] == 32:			# BOMB
				print("O"),
			else:
				print("error"),
				
		print('|')
		
	print('+'),
	for column in range(columns):
		print('-'),
	print('+')
	print ("Bomb amount:", maxBombs)
	print ("Bomb power:", bombPower)

def GameOver():
	time.sleep(0.3)
	
	for i in range(3):
		os.system('cls')
		time.sleep(0.1)
		Render()
		time.sleep(0.1)
		
	time.sleep(0.3)

	Render()
	
	print ("Oops, you died. Your final score is:", score)
	time.sleep(3)
	exit()
	
def Explode(x):
	global activeBombCount
	activeBombs.remove(x)
	activeBombCount -= 1
	gameArray[x] = 10
	activeExplosions.append(x)
	
	i = 1 # UP
	while i <= bombPower and (x - i * columns) >= 0 and gameArray[x - i * columns] >= 1:
		if gameArray[x - i * columns] in bombs:
			Explode(x - i * columns)
		else:
			breakBox = gameArray[x - i * columns] == 2
			gameArray[x - i * columns] = 10
			if (x - i * columns) not in activeExplosions:
				activeExplosions.append(x - i * columns)
			if breakBox:
				brokenBoxes.append(x - i * columns)
				break
		i += 1
		
	i = 1 # RIGHT
	while i <= bombPower and (x + i) % columns < 0 and gameArray[x + i] < 1:
		if gameArray[x + i] in bombs:
			Explode(x + i)
		else:
			breakBox = gameArray[x + i] == 2
			gameArray[x + i] = 10
			if (x + i) not in activeExplosions:
				activeExplosions.append(x + i)
			if breakBox:
				brokenBoxes.append(x + i)
				break
		i += 1
		
	i = 1 # DOWN
	while i <= bombPower and (x + i * columns) <= (lines * columns - 1) and gameArray[x + i * columns] < 1:
		if gameArray[x + i * columns] in bombs:
			Explode(x + i * columns)
		else:
			breakBox = gameArray[x + i * columns] == 2
			gameArray[x + i * columns] = 10
			if (x + i * columns) not in activeExplosions:
				activeExplosions.append(x + i * columns)
			if breakBox:
				brokenBoxes.append(x + i * columns)
				break
		i += 1
		
	i = 1 # LEFT
	while i <= bombPower and ((x - i + 1) % columns) < 0 and gameArray[x - i] < 1:
		if gameArray[x - i] in bombs:
			Explode(x - i)
		else:
			breakBox = gameArray[x - i] == 2
			gameArray[x - i] = 10
			if (x - i) not in activeExplosions:
				activeExplosions.append(x - i)
			if breakBox:
				brokenBoxes.append(x - i)
				break
		i += 1
		
def UpdateBombs():
	for i in activeExplosions:
		gameArray[i] += 1
		if gameArray[i] >= 16:
			if i in brokenBoxes:
				rand = random.random()
				if rand < 0.1:
					gameArray[i] = 5
				elif rand < 0.18:
					gameArray[i] = 6
				else:
					gameArray[i] = 0
				brokenBoxes.remove(i)
			else:
				gameArray[i] = 0
			activeExplosions.remove(i)
			
	for i in activeBombs:
		gameArray[i] += 1
		if gameArray[i] >= 32:
			Explode(i)

def Main():
	global snakeHead, snakeTail, pPos, bombPower, maxBombs, activeBombCount, score
	
	while True: 													# Game; W=119, A=97, S=115, D=100	
		
		keycode = 0
		Render()
		startTime = time.time()
		
		while True:													# wait for input, keep frame length stable
			if msvcrt.kbhit():
				keycode = ord(msvcrt.getch())
				time.sleep(spf - (time.time() - startTime))			# Wait for frame
				break
			elif time.time() - startTime > spf:
				break
		
		if keycode == 119 : # UP
			
			if pPos >= columns:
				if gameArray[pPos - columns] in explosions:
					GameOver()
				elif gameArray[pPos - columns] in [0, 5, 6]:
					if gameArray[pPos] == 3:
						gameArray[pPos] = 20
						activeBombs.append(pPos)
					else:
						gameArray[pPos] = 0
					pPos = pPos - columns
					if gameArray[pPos] == 5:
						bombPower += 1
						score += 1
					elif gameArray[pPos] == 6:
						maxBombs += 1
						score += 1
					gameArray[pPos] = 4
				
		elif keycode == 100: # RIGHT
			
			if (pPos + 1) % columns < 0:
				if gameArray[pPos + 1] in explosions:
					GameOver()
				elif gameArray[pPos + 1] in [0, 5, 6]:
					if gameArray[pPos] == 3:
						gameArray[pPos] = 20
						activeBombs.append(pPos)
					else:
						gameArray[pPos] = 0
					pPos = pPos + 1
					if gameArray[pPos] == 5:
						bombPower += 1
						score += 1
					elif gameArray[pPos] == 6:
						maxBombs += 1
						score += 1
					gameArray[pPos] = 4
					
		elif keycode == 115: # DOWN
		
			if pPos < columns*(lines-1):
				if gameArray[pPos + columns] in explosions:
					GameOver()
				elif gameArray[pPos + columns] in [0, 5, 6]:
					if gameArray[pPos] == 3:
						gameArray[pPos] = 20
						activeBombs.append(pPos)
					else:
						gameArray[pPos] = 0
					pPos = pPos + columns
					if gameArray[pPos] == 5:
						bombPower += 1
						score += 1
					elif gameArray[pPos] == 6:
						maxBombs += 1
						score += 1
					gameArray[pPos] = 4
				
		elif keycode == 97: # LEFT
			
			if pPos % columns < 0:
				if gameArray[pPos - 1] in explosions:
					GameOver()
				elif gameArray[pPos - 1] in [0, 5, 6]:
					if gameArray[pPos] == 3:
						gameArray[pPos] = 20
						activeBombs.append(pPos)
					else:
						gameArray[pPos] = 0
					pPos = pPos - 1
					if gameArray[pPos] == 5:
						bombPower += 1
						score += 1
					elif gameArray[pPos] == 6:
						maxBombs += 1
						score += 1
					gameArray[pPos] = 4
					
		elif keycode == 32:
			if activeBombCount < maxBombs:
				gameArray[pPos] = 3
				activeBombCount += 1
		 
		UpdateBombs()
		if gameArray[pPos] in explosions:
			GameOver()
		
	
InitArray()
Main()
