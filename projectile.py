import pygame as pg
import math

class Projectile:
    def __init__(self, x, y, angle, speed):
        self.pos = pg.Vector2(x, y)
        self.tPos = pg.Vector2(x, y)
        self.vel = pg.Vector2(speed * math.cos(angle * math.pi / 180), speed * -math.sin(angle * math.pi / 180))

    def update(self):
        self.pos += self.vel

    def draw(self, screen):
        pass
    
    def translate(self, point):
        self.tPos = self.pos - point

class Bullet(Projectile):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 50)
        self.lifeSpan = 60
    
    def update(self, blocks):
        super().update()
        self.lifeSpan -= 1
        self.collide(blocks)

    def draw(self, screen):
        pg.draw.line(screen, (255,200,0), self.tPos - self.vel, self.tPos, 5)

    def collide(self, blocks):
        for block in blocks:
            # if block.image.get_rect().collidepoint((self.pos.x, self.pos.y)):
            if self.pos.x > block.pos.x and self.pos.x < block.pos.x + block.width and self.pos.y > block.pos.y and self.pos.y < block.pos.y + block.height:
                self.lifeSpan = 0

class Hook(Projectile):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, 20)
        self.isStuck = False
    
    def update(self, blocks):
        if not self.isStuck:
            super().update()
            self.collide(blocks)
    
    def draw(self, screen, pos):
        pg.draw.line(screen, (50,50,50), self.tPos, pos, 3)

    def collide(self, blocks):
        for block in blocks:
            # if block.image.get_rect().collidepoint((self.pos.x, self.pos.y)):
            if self.pos.x > block.pos.x and self.pos.x < block.pos.x + block.width and self.pos.y > block.pos.y and self.pos.y < block.pos.y + block.height:
                self.isStuck = True