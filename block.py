from pygame.constants import HIDDEN
from perlin import PerlinNoiseFactory
import pygame as pg

class Block:
    def __init__(self, x, y, w, h):
        self.pos = pg.Vector2(x, y)
        self.tPos = pg.Vector2(x, y)
        self.width = w
        self.height = h
        self.image = pg.image.load('blocks/metal.png').convert()
        self.image = pg.transform.scale(self.image, (self.width, self.height))
    
    def draw(self, screen):
        screen.blit(self.image, (self.tPos.x, self.tPos.y))
    
    def translate(self, point):
        self.tPos = self.pos - point
    
    def isVisible(self, screenWidth, screenHeight):
        return self.tPos.x > -self.width and self.tPos.x < screenWidth and self.tPos.y > -self.height and self.tPos.y < screenHeight

def generateMap(filePath) -> list:
    blockList = []
    file = open(filePath, 'r')
    strArr = [line for line in file]
    for i in range(len(strArr)):
        for j in range(len(strArr[i])):
            if strArr[i][j] == '#':
                blockList.append(Block(j * 32, i * 32, 32, 32))
    return blockList

def generateTerrain(width, height) -> list:
    noise = PerlinNoiseFactory(1, width)
    blockList = []
    for i in range(width):
        y = round(height - noise(i/width) * height * 2)
        blockList.append(Block(i * 32, y * 32, 32, 32))
        for j in range(height - y + 10):
            blockList.append(Block(i * 32, (y + j) * 32, 32, 32))

    return blockList