import random
from time import sleep

import pygame
from pygame.locals import *

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


class Snake(pygame.sprite.Sprite):

    x = 0
    y = 0
    speed = 3
    length = []
    length_pos = []

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.snake_pic = pygame.image.load(image).convert()
        self.rect = self.snake_pic.get_rect()
        self.image = pygame.Surface(self.snake_pic.get_rect().bottomright)
        self.length.append(self.snake_pic)
        self.length_pos.append(self.rect.topleft)

    def moveDown(self):
        self.y = self.y + self.speed
        self.rect = Rect(
            self.x,
            self.y,
            self.snake_pic.get_rect().bottom,
            self.snake_pic.get_rect().right)
        for i in range(len(self.length)):
            self.length_pos[i] = (self.x, self.y+(self.rect.width*i))

    def moveUp(self):
        self.y = self.y - self.speed
        self.rect = Rect(
            self.x,
            self.y,
            self.snake_pic.get_rect().bottom,
            self.snake_pic.get_rect().right)
        for i in range(len(self.length)):
            self.length_pos[i] = (self.x, self.y+(self.rect.width*i))

    def moveRight(self):
        self.x = self.x + self.speed
        self.rect = Rect(
            self.x,
            self.y,
            self.snake_pic.get_rect().bottom,
            self.snake_pic.get_rect().right)
        for i in range(len(self.length)):
            self.length_pos[i] = (self.x+(self.rect.width*i), self.y)

    def moveLeft(self):
        self.x = self.x - self.speed
        self.rect = Rect(
            self.x,
            self.y,
            self.snake_pic.get_rect().bottom,
            self.snake_pic.get_rect().right)
        for i in range(len(self.length)):
            self.length_pos[i] = (self.x+(self.rect.width*i), self.y)

    def update(self, direct):
        self.direct = direct
        if self.direct == "down":
            self.moveDown()
        if self.direct == "up":
            self.moveUp()
        if self.direct == "right":
            self.moveRight()
        if self.direct == "left":
            self.moveLeft()

    def grow(self):
        self.length.append(self.snake_pic)
        self.length_pos.append(
            (self.rect.top+(self.rect.width*len(self.length)),
            self.rect.left+(self.rect.width*len(self.length))))

class Food(pygame.sprite.Sprite):
    x = random.randrange(10, SCREEN_WIDTH - 100)
    y = random.randrange(10, SCREEN_HEIGHT - 100)
    food_tally = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.food_pic = pygame.image.load("assets/burgerp.png").convert()
        self.rect = self.food_pic.get_rect()
        self.image = pygame.Surface(self.food_pic.get_rect().bottomright)

    def checkCollision(self, sprite1, sprite2):
        col = pygame.sprite.collide_rect(sprite1, sprite2)
        if col is True:
            self.Posx()
            self.Posy()

    def Posx(self):
        self.x = random.randrange(10, 500)
        self.rect = Rect(
            self.x,
            self.y,
            self.food_pic.get_rect().bottom,
            self.food_pic.get_rect().right)

    def Posy(self):
        self.y = random.randrange(10, 500)
        self.rect = Rect(
            self.x,
            self.y,
            self.food_pic.get_rect().bottom,
            self.food_pic.get_rect().right)

class App:
    x = 100
    y = 100
    snake = 0
    food = 0
    direct = "right"

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.snake = Snake("assets/bob.png")
        self.food = Food()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0,0,0))
        for i in range(len(self.snake.length)):
            self._display_surf.blit(self.snake.length[i],self.snake.length_pos[i])
        self._display_surf.blit(self.food.food_pic,(self.food.x,self.food.y))
        self.snake.update(self.direct)
        pygame.display.flip()
        sleep(0.03)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]: #"try" in case another button is pressed
                self.direct = "right"

            if keys[K_LEFT]:
                self.direct = "left"

            if keys[K_UP]:
                self.direct = "up"

            if keys[K_DOWN]:
                self.direct = "down"

            if pygame.sprite.collide_rect(self.snake, self.food):
                self.food.Posy()
                self.food.Posx()
                self.food.food_tally += 1
                if self.food.food_tally%5 == 0:
                    self.snake.speed += 1
                    self.snake.grow()

            if self.snake.x > 520 or self.snake.y > 520:
                self.snake.speed = 1
                self.food.tally = 0
                self.snake.x = 0
                self.snake.y = 0
                del self.snake.length[:]
            if self.snake.x < 0 or self.snake.y < 0:
                self.snake.speed = 1
                self.food.tally = 0
                self.snake.x = 0
                self.snake.y = 0
                del self.snake.length[:]

            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
