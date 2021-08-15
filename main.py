import pygame as pg, sys

from player import Player
from block import *

class App:
    def __init__(self) -> None:
        pg.init()
        self.size = self.width, self.height = 800, 480
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption('Platformer')

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
        self.platforms = generateMap('levels/level.txt')
        
    def main_loop(self) -> None:
        # set background to light blue
        self.screen.fill((100, 150, 255))
        
        # update player
        self.player.update()
        self.player.useWeapon(self.platforms)

        visiblePlatforms = [platform for platform in self.platforms if platform.isVisible(self.width, self.height)]
        # collision with platforms
        self.player.onGround = False
        for platform in visiblePlatforms:
            if self.player.collide(platform):
                self.player.onGround = True

        self.player.jump()

        if self.player.pos.y > 1000:
            self.player.respawn()

        # draw player
        self.player.translate(pg.Vector2(self.player.pos.x - self.width/2 + self.player.width, self.player.pos.y - 300))
        self.player.draw(self.screen)

        # draw platforms
        for platform in self.platforms:
            platform.translate(pg.Vector2(self.player.pos.x - self.player.tPos.x, self.player.pos.y - self.player.tPos.y))
            if platform.isVisible(self.width, self.height):
                platform.draw(self.screen)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
    
    def user_interface(self):
        self.player.drawHud(self.screen)

            
App().run()
