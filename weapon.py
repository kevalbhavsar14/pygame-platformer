from math import dist
import pygame as pg
from projectile import *
from block import Block

class Weapon:
    def __init__(self, image):
        self.image = pg.image.load(image).convert_alpha()
        self.image = pg.transform.scale(self.image, (64,32))
    
    def fire(self, x, y, angle):
        pass

    def update(self):
        pass

    def draw(self, screen, aim, pos: pg.Vector2, tPos: pg.Vector2):
        pass

class Gun(Weapon):
    def __init__(self):
        super().__init__('weapons/ak.png')
        self.fireRate = 0.1
        self.fireTimer = 0
        self.bullets = []
    
    def fire(self, x, y, angle):
        self.fireTimer += self.fireRate
        if self.fireTimer >= 1: 
            self.fireTimer = 0
            self.bullets.append(Bullet(x, y, angle))
    
    def update(self, pos, blocks):
        for bullet in self.bullets:
            bullet.update(blocks)
            if bullet.lifeSpan < 0:
                self.bullets.remove(bullet)

    def draw(self, screen, aim, pos: pg.Vector2, tPos: pg.Vector2):
        for bullet in self.bullets:
            bullet.translate(pg.Vector2(pos.x - tPos.x, pos.y - tPos.y))
            bullet.draw(screen)

        weapon = self.image if aim < 90 and aim > -90 else pg.transform.flip(self.image, True, False)
        if aim < 90 and aim > -90:
            angle = aim
            posX = tPos.x
        else:
            angle = -180 + aim
            posX = tPos.x - 32
        if aim > 0:
            posY = tPos.y + 25 - (abs(angle * 0.7))
        else:
            posY = tPos.y + 25
        weapon = pg.transform.rotate(weapon, angle)

        screen.blit(weapon, (posX, posY))

class Grapple(Weapon):
    def __init__(self):
        super().__init__('weapons/grapple.png')
        self.hook = None
    
    def fire(self, x, y, angle):
        self.hook = Hook(x , y , angle)
    
    def update(self, pos, blocks):
        if self.hook:
            self.hook.update(blocks)
            d = dist([self.hook.pos.x, self.hook.pos.y], [pos.x, pos.y])
            if pg.key.get_pressed()[pg.K_s] or d > 500:
                self.hook = None
                return None
            if self.hook.isStuck:
                vel = pg.Vector2(self.hook.pos - pos)
                vel.scale_to_length(20)
                if d < 50  or pg.key.get_pressed()[pg.K_s]:
                    self.hook = None
                return vel
            return None
    
    def draw(self, screen, aim, pos: pg.Vector2, tPos: pg.Vector2):
        if self.hook:
            self.hook.translate(pg.Vector2(pos.x - tPos.x, pos.y - tPos.y))
            self.hook.draw(screen, tPos + pg.Vector2(16, 32))

        weapon = self.image if aim < 90 and aim > -90 else pg.transform.flip(self.image, True, False)
        if aim < 90 and aim > -90:
            angle = aim
            posX = tPos.x
        else:
            angle = -180 + aim
            posX = tPos.x - 32
        if aim > 0:
            posY = tPos.y + 25 - (abs(angle * 0.7))
        else:
            posY = tPos.y + 25
        weapon = pg.transform.rotate(weapon, angle)

        screen.blit(weapon, (posX, posY))