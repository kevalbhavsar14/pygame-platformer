import pygame as pg
from weapon import *
from block import Block

class Player:
    def __init__(self, x, y):
        # size, position and movement
        self.width = 32
        self.height = 64
        self.spawn = pg.Vector2(x, y)
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)
        self.acc = pg.Vector2(0, 0)
        self.tPos = pg.Vector2(400 - self.width/2, 300)
        
        # textures
        self.idle = pg.transform.scale(pg.image.load('player/idle.png').convert_alpha(), (self.width, self.height))
        walk1 = pg.transform.scale(pg.image.load('player/walk1.png').convert_alpha(), (self.width, self.height))
        walk2 = pg.transform.scale(pg.image.load('player/walk2.png').convert_alpha(), (self.width, self.height))
        self.walk = [walk1, walk2]
        self.walkIx = 0.0

        self.image = self.idle
        self.image = pg.transform.scale(self.image, (self.width, self.height))

        # equipment
        self.inventory = [Gun(), Grapple(), None]
        self.weaponIndex = 0
        self.weapon = self.inventory[self.weaponIndex]
        
        # states
        self.onGround = False
        self.isWalking = False
        self.isSprinting = False
        self.aim = 0

        # stats
        self.maxHealth = 20
        self.health = self.maxHealth
        self.fallHeight = 0
        self.takingDmg = False
    
    def update(self):
        maxVel = 20
        self.pos += self.vel
        self.vel += self.acc
        self.acc.update(0, 0)
        if self.vel.length() > maxVel:
            self.vel.scale_to_length(maxVel)
        if self.health <= 0:
            self.respawn()
        
        self.aim = (pg.Vector2(pg.mouse.get_pos()) - (self.tPos + pg.Vector2(0,30))).angle_to(pg.Vector2(0,0))

        self.move()
    
    def applyForce(self, force):
        self.acc += force
    
    def collide(self, object):
        onGround = False
        # top
        if self.pos.y + self.height >= object.pos.y and self.pos.y + self.height - 20 < object.pos.y and self.pos.x + self.width > object.pos.x + 5 and self.pos.x < object.pos.x + object.width - 5:
            self.pos.y = object.pos.y - self.height
            # self.takeDamage(self.fallHeight // 40)
            self.vel.y = 0
            onGround = True
            self.fallHeight = 0
        # bottom
        if self.pos.y <= object.pos.y + object.height - 10 and self.pos.y > object.pos.y + object.height - 20 and self.pos.x + self.width > object.pos.x + 5 and self.pos.x < object.pos.x + object.width - 5:
            self.pos.y = object.pos.y + object.height
            self.vel.y = 0
        # left
        if self.pos.x + self.width >= object.pos.x and self.pos.x + self.width < object.pos.x + 20 and self.pos.y > object.pos.y - self.height and self.pos.y < object.pos.y + object.height:
            self.pos.x = object.pos.x - self.width
            self.vel.x = 0
        # right
        if self.pos.x <= object.pos.x + object.width - 5 and self.pos.x > object.pos.x + object.width - 20 and self.pos.y + self.height > object.pos.y and self.pos.y < object.pos.y + object.height:
            self.pos.x = object.pos.x + object.width
            self.vel.x = 0
        return onGround

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.pos += pg.Vector2(-5, 0)
            self.isWalking = True
            if keys[pg.K_LSHIFT]:
                self.pos += pg.Vector2(-5, 0)
                self.isSprinting = True
            else:
                self.isSprinting = False

        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.pos += pg.Vector2(5, 0)
            self.isWalking = True
            if keys[pg.K_LSHIFT]:
                self.pos += pg.Vector2(5, 0)
                self.isSprinting = True
            else:
                self.isSprinting = False
        else:
            self.isWalking = False
        
    def jump(self):
        if pg.key.get_pressed()[pg.K_SPACE] and self.onGround:
            self.onGround = False
            self.vel = pg.Vector2(0, -15)
    
    def respawn(self):
        self.pos.update(self.spawn)
        self.health = self.maxHealth
        self.fallHeight = 0
    
    def takeDamage(self, dmg):
        if dmg < 0: dmg = 0
        self.health -= dmg
        self.health = 0 if self.health < 0 else self.health
        if dmg > 0:
            self.takingDmg = True
        else:
            self.takingDmg = False
    
    def useWeapon(self, blocks):
        if self.weapon:
            if pg.mouse.get_pressed()[0]:
                self.weapon.fire(self.pos.x + self.width/2, self.pos.y + self.height/2, self.aim)
            pull = self.weapon.update(self.pos, blocks)
            if pull:
                self.applyForce(pull)
    
    def placeBlock(self, blocks):
        x, y = pg.mouse.get_pos()
        x += self.pos.x - self.tPos.x
        y += self.pos.y - self.tPos.y
        x, y = (x // 32) * 32, (y // 32) * 32
        for block in blocks:
            if block.pos.x == x and block.pos.y == y:
                return None
        return Block(x, y, 32, 32, 'metal')

    def draw(self, screen):
        self.animation()

        image = self.image.copy() if self.aim < 90 and self.aim > -90 else pg.transform.flip(self.image, True, False)
        if self.takingDmg: image.fill((255,0,0))
        self.takingDmg = False
        screen.blit(image, (self.tPos.x, self.tPos.y))
        if self.weapon: self.weapon.draw(screen, self.aim, self.pos, self.tPos)
        
    def translate(self, point):
        self.tPos = self.pos - point
    
    def animation(self):
        if not self.onGround:
            self.image = self.walk[0]
        elif self.isWalking:
            self.image = self.walk[int(self.walkIx)]
            self.walkIx += 0.2 if self.isSprinting else 0.1
            if self.walkIx >= len(self.walk):
                self.walkIx = 0
        else:
            self.image = self.idle
    
    def drawHud(self, screen):
        # health
        bg = pg.Surface((200,20))
        bg.fill((100,100,100))
        hp = pg.Surface((self.health * 10, 20))
        hp.fill((255,50,50))
        screen.blit(bg, (10,10))
        screen.blit(hp, (10,10))