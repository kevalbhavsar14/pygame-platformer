import pygame as pg, sys

from player import Player
from block import *

class App:
    def __init__(self) -> None:
        pg.init()
        self.size = self.width, self.height = 800, 480
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption('blocker')

    def run(self) -> None:
        self.setup()
        while True:
            self.handle_events()
            self.main_loop()
            self.user_interface()
            pg.display.update()
            pg.time.Clock().tick(60)
            
    def setup(self) -> None:
        self.player = Player(100, 300)
        self.gravity = pg.Vector2(0, 1)
        
        self.blocks = generateTerrain(100, 15)
        self.camera = pg.Vector2(0, 0)

        # backgournd
        sky = pg.transform.scale(pg.image.load('background/sky.png').convert_alpha(), (self.width, self.height))
        mountains = pg.transform.scale(pg.image.load('background/mountains.png').convert_alpha(), (self.width, self.height))
        ground = pg.transform.scale(pg.image.load('background/ground.png').convert_alpha(), (self.width, self.height))
        overlay = pg.transform.scale(pg.image.load('background/overlay.png').convert_alpha(), (self.width, self.height))
        self.background = {'sky':sky, 'mountains':mountains, 'ground':ground, 'overlay':overlay}

    def main_loop(self) -> None:

        # set background
        self.screen.blit(self.background['sky'], (0, 0))
        self.screen.blit(self.background['mountains'], (-(self.camera.x / 10) % self.width, 0))
        self.screen.blit(self.background['mountains'], (-(self.camera.x / 10) % self.width - self.width, 0))
        self.screen.blit(self.background['ground'], (-(self.camera.x / 5) % self.width, 0))
        self.screen.blit(self.background['ground'], (-(self.camera.x / 5) % self.width - self.width, 0))
        self.screen.blit(self.background['overlay'], (0, 0))
        
        # update player
        self.player.applyForce(self.gravity)
        self.player.update()
        self.player.useWeapon(self.blocks)

        for block in self.blocks:
            block.translate(self.camera)
        self.visibleBlocks = [block for block in self.blocks if block.isVisible(self.width, self.height)]
        # collision with blocks
        self.player.onGround = False
        for block in self.visibleBlocks:
            if self.player.collide(block):
                self.player.onGround = True

        self.player.jump()

        if self.player.pos.y > 1000:
            self.player.respawn()

        self.camera = self.player.pos - self.player.tPos
        # draw player
        self.player.translate(pg.Vector2(self.player.pos.x - self.width/2 + self.player.width, self.player.pos.y - 300))
        self.player.draw(self.screen)

        # draw blocks
        for block in self.visibleBlocks:
            block.draw(self.screen)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    self.player.weaponIndex = (self.player.weaponIndex + 1) % len(self.player.inventory)
                    self.player.weapon = self.player.inventory[self.player.weaponIndex]
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_RIGHT:
                    block = self.player.placeBlock(self.visibleBlocks)
                    if block: self.blocks.append(block)
    
    def user_interface(self):
        self.player.drawHud(self.screen)

            
App().run()
