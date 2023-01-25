from typing import List

import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from pygame.locals import *

clock = pygame.time.Clock()
FPS = 60

class ScreenInterface:

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        ...

    def update(self) -> None:
        ...

    def draw(self, surface: pygame.Surface) -> None:
        ...


#================================================================================================


class PauseScreen:

    def __init__(self, parent: ScreenInterface):
        self.parent = parent

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    Game.set_screen(self.parent)

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.parent.draw(surface)

        background = pygame.Surface((Game.WIDTH, Game.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(background, (0, 0, 0, 128),
                         (0, 0, Game.WIDTH, Game.HEIGHT))

        surface.blit(background, (0, 0))


#================================================================================================


class Level_1:
    
    def __init__(self) -> None:
        #background
        self.background = pygame.image.load("Battle_background.jpg")
        self.background = pygame.transform.scale(self.background, (1920, 1080))
        #<a href="https://www.freepik.com/free-vector/ancient-architecture-with-arches-torches_22444977.htm#query=dungeon%20background&position=0&from_view=keyword">Image by upklyak</a> on Freepik

        #variables
        self.ground = 965
        self.fighter_x = 810
        self.fighter_y = 710
        self.boss_x = 1750
        self.boss_y = 710
        self.fighter_speed = 30
        self.jumping = False
        self.jump_height = 10
        self.vel_y = self.jump_height
        self.attack_type = 0
        self.attack_effect = 0
        self.attack_radius = 0
        self.attack_cooldown = 0
        self.boss_hp = 100
        self.fighter_hp = 100
        self.boss_move = 0
        self.boss_speed = 30
        self.fighter_hit = False
        self.fighter_sprite = pygame.image.load('fighter.png')
        self.boss_sprite = pygame.image.load('boss.png)

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Game.set_screen(ScreenTwo())
                print("Click")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    Game.set_screen(PauseScreen(self))

        
    def update(self) -> None:
        clock.tick(FPS)
        self.attack_cooldown -= 1

        #distance claculation
        distance = ((self.fighter_x - self.boss_x) ** 2 + (self.fighter_y - self.boss_y) ** 2) ** (1/2)

        #game detect
        if self.boss_hp <= 0:
            print('fighter wins')
            print('hp:', self.boss_hp, self.fighter_hp)
            exit()
        if self.fighter_hp <= 0:
            print('fighter loses')
            print('hp:', self.boss_hp, self.fighter_hp)
            exit()

        #boss
        self.boss_move = self.boss_move * 0.9 + (self.fighter_x - self.boss_x) * 0.1
        self.boss_x += (self.boss_move / abs(self.boss_move)) * min(abs(self.boss_move), self.boss_speed)
        if self.boss_speed < self.fighter_speed:
            self.boss_speed += 1
        if distance < 100:
            self.fighter_hit = True
            self.fighter_hp -= 1


        #keypress
        keys = pygame.key.get_pressed()

        #left, right movement
        if keys[pygame.K_a]:
            self.fighter_x -= self.fighter_speed
        if keys[pygame.K_d]:
            self.fighter_x += self.fighter_speed 

        #jump
        if keys[pygame.K_SPACE] and self.jumping == False:
            self.jumping = True

        #stay on screen
        if self.fighter_y >= 1080:
            self.fighter_y -= self.fighter_speed
        if self.fighter_x <= 0:
            self.fighter_x += self.fighter_speed
        if self.fighter_x >= 1910:
            self.fighter_x -= self.fighter_speed
        
        #falling off screen
        if self.jumping:
            self.fighter_y -= self.jump_height*3
            self.jump_height -= 1
            if self.jump_height < -10:
                self.jumping = False
                self.jump_height = 10

        #attack detection
        if (keys[pygame.K_w] or keys[pygame.K_s]) and self.attack_cooldown <= 0:
            if keys[pygame.K_w]:
                self.attack_type = 1
                self.attack_cooldown = 10
            if keys[pygame.K_s]:
                self.attack_type = 2
                self.attack_cooldown = 100

        #attacking
        if self.attack_type:
            if distance < 300:
                self.attack_radius = 200
                self.attack_effect = self.attack_type
                if self.attack_type == 2:
                    self.boss_speed = 1
                self.boss_hp -= self.attack_type
            self.attack_type = 0



    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0,0))

        pygame.draw.rect(surface, (0, 0, 255), (10, 10, 10 + 540 * (self.fighter_hp) / 100, 50)) #main fighter hp
        pygame.draw.rect(surface, (0, 255, 0), (10, 60, 10 + 540 * (self.boss_hp) / 100, 50)) #the boss hp

        """
        pygame.draw.rect(surface, (0, 0, 255), (self.fighter_x, self.fighter_y, 125, 250)) #main fighter character
        pygame.draw.rect(surface, (0, 255, 0), (self.boss_x, self.boss_y, 125, 250)) # the boss
        """
        surface.blit(self.fighter_sprite, (self.fighter_x, self.fighter_y, 125, 250))
        surface.blit(self.boss_sprite, (self.boss_x, self.boss_y, 125, 250))

        #attack stuff
        attack_color = {1: (255, 0, 0), 2: (255, 255, 0)}
        if self.fighter_hit:
            self.fighter_hit = False
            pygame.draw.circle(surface, (255, 255, 255), (self.fighter_x, self.fighter_y), 100)
        if self.attack_effect:
            pygame.draw.circle(surface, attack_color[self.attack_effect], (self.boss_x, self.boss_y), self.attack_radius)
            if self.attack_radius > 0:
                self.attack_radius -= 5
            else:
                self.attack_effect = 0
        
#================================================================================================


class main_menu:

    def __init__(self) -> None:
        self.circle_x = 500
        self.circle_y = 100
        self.black = (0, 0, 0)
        self.blue = 0, 255, 0
        self.green = 71, 148, 58
        self.yellow = 255, 223, 0
        self.red = 255, 0, 0
        self.game1_button = pygame.Rect(50, 300, 100, 190)
        self.game2_button = pygame.Rect(175, 425, 150, 65)
        self.game3_button = pygame.Rect(425, 425, 150, 65)
        self.game4_button = pygame.Rect(600, 325, 100, 165)
        self.click = False

    def handle_events(self, events: List[pygame.event.Event]) -> None:
            mx, my = pygame.mouse.get_pos()
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if self.game1_button.collidepoint((mx, my)):
                        Game.set_screen(Level_1())
                    if self.game2_button.collidepoint((mx, my)):
                        Game.set_screen(Level_2())
                    if self.game3_button.collidepoint((mx, my)):
                        Game.set_screen(Level_3())
                    if self.game4_button.collidepoint((mx, my)):
                        Game.set_screen(Level_4())


    def update(self) -> None:
            self.circle_x += 0

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((255, 255, 255))  # always the first drawing command
        pygame.draw.circle(surface, (0, 255, 0), (self.circle_x, self.circle_y), 30)

        pygame.draw.rect(surface, self.red, self.game1_button)
        pygame.draw.rect(surface, self.blue, self.game2_button)
        pygame.draw.rect(surface, self.yellow, self.game3_button)
        pygame.draw.rect(surface, self.green, self.game4_button)

#================================================================================================


class Game:
    instance: 'Game'
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(self.SIZE)
        self.clock = pygame.time.Clock()

        self.current_screen = main_menu()

        Game.instance = self

    @classmethod
    def set_screen(cls, new_screen: ScreenInterface):
        cls.instance.current_screen = new_screen

    def run(self):
        running = True
        while running:
            # EVENT HANDLING
            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False

            self.current_screen.handle_events(events)
            self.current_screen.update()
            self.current_screen.draw(self.screen)

            # Must be the last two lines
            # of the game loop
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
