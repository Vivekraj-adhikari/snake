import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')
font = pygame.font.Font('arial.ttf', 25)

BLOCK_SIZE = 20
GAME_SPEED = 15

# rgb colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

class SnakeGame:
    def __init__(self, w = 640, h = 480):
        self.w = w
        self.h = h
        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("PySnake")
        self.clock = pygame.time.Clock()

        #init initial game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y), 
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
    
    def _place_food(self):
        x = random.randint(BLOCK_SIZE, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(BLOCK_SIZE, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def _play_step(self):
        # user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # move
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        # update pygame and clock
        self._update_ui()
        self.clock.tick(GAME_SPEED)

        # return game_over and score
        return game_over, self.score

    def _is_collision(self):
        if self.head.x < 0 or self.head.x > self.w - BLOCK_SIZE or self.head.y < 0 or self.head.y > self.h - BLOCK_SIZE:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        
        self.head = Point(x, y)

    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.circle(self.display, BLUE1, [pt.x, pt.y], BLOCK_SIZE / 2)
            pygame.draw.circle(self.display, BLUE2, [pt.x, pt.y], BLOCK_SIZE / 2 - 3)
        
        pygame.draw.circle(self.display, RED, [self.food.x, self.food.y], BLOCK_SIZE / 2)

        text = font.render(f'Score: {self.score}', True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

if __name__=='__main__':
    snake = SnakeGame()
    while True:
        game_over, score = snake._play_step()
        if game_over:
            break
    pygame.quit()