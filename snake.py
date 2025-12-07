import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')
font = pygame.font.Font('arial.ttf', 25)

BLOCK_SIZE = 20
GAME_SPEED = 5

# rgb colors
WHITE = (255, 255, 255)
RED = (204, 86, 101)
BLUE1 = (7, 97, 39)
BLUE2 = (61, 184, 104)
BLACK = (0, 0, 0)

class SnakeGame:
    def __init__(self, w = 640, h = 480):
        self.w = w
        self.h = h
        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("PySnake")
        self.clock = pygame.time.Clock()

        self.reset()
        self.frame_iteration = 0

    def reset(self):
        #init initial game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y), 
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
    
    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def _play_step(self, action):
        self.frame_iteration += 1
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
        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0
        # check if game over
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        # update pygame and clock
        self._update_ui()
        self.clock.tick(GAME_SPEED)

        # return game_over and score
        return reward,game_over, self.score

    def is_collision(self, pt):
        if pt.x < 0 or pt.x > self.w - BLOCK_SIZE or pt.y < 0 or pt.y > self.h - BLOCK_SIZE:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def _move(self, action):
        #direction
        clkwise_direction = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clkwise_direction.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clkwise_direction[index]
        elif np.array_equal(action, [0, 1, 0]):
            new_idx = (index + 1) % 4
            new_direction = clkwise_direction[new_idx]
        else:
            if index == 0:
                new_idx = 3
            else:
                new_idx = (index - 1) % 4
            new_direction = clkwise_direction[new_idx]
        
        self.direction = new_direction

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        
        self.head = Point(x, y)

    def _update_ui(self):
        self.display.fill(WHITE)
        for pt in self.snake:
            pygame.draw.circle(self.display, BLUE1, [pt.x, pt.y], BLOCK_SIZE / 2)
            pygame.draw.circle(self.display, BLUE2, [pt.x, pt.y], BLOCK_SIZE / 2 - 3)
        
        pygame.draw.circle(self.display, RED, [self.food.x, self.food.y], BLOCK_SIZE / 2)

        text = font.render(f'Score: {self.score}', True, BLACK)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
