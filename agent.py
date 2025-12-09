import torch
import random
import numpy as np
from snake import SnakeGame, Direction, Point
from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY)

    def get_state(self, game):
        head = game.snake[0]

        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # danger straight
            (dir_l and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),
            # danger right
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)) or
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)),
            # danger left
            (dir_l and game.is_collision(point_d)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_d and game.is_collision(point_r)),
            # move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            # food placement
            game.food.x < head.x,
            game.food.x > head.x,
            game.food.y < head.y,
            game.food.y > head.y
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = []
    best_score = []

    agent = Agent()
    game = SnakeGame()

    while True:
        # get current state
        state_old = agent.get_state()

        # get action for that state
        final_move = agent.get_action(state_old)

        # play the game using that action
        reward, done, score = game._play_step(final_move)

        # get new state
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            #train long memory
            #plot results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > best_score:
                best_score = score
                # agent.model.save
            
            print(f"Game: {agent.n_games}, Score: {score}, Highest_Score: {best_score}")



if __name__=='__main__':
    train()