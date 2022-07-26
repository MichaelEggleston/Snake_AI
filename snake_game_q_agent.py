import math
from os import stat
from numpy import block
import pygame as pg
import random
import time
import matplotlib.pyplot as plt

from Q_model import Q_model

class Snake():
    def __init__(self, screen_width = 0, screen_height = 0):
        super().__init__()
        self.x_pos = screen_width/2
        self.y_pos = screen_height/2
        self.width = 10
        self.height = 10
        self.velocity = 10
        self.direction = 'stop'
        self.previous_dirs = []
        self.body = []
        self.body_rgb = [0, 255, 0]
        self.head_rgb = [0, 255, 0]
        self.head = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)
    
    def add_body(self):
        if len(self.body) == 0:
            self.body.insert(0, pg.Rect(self.head.x, self.head.y, self.width, self.height))
        else:
            self.body.insert(-1, pg.Rect(self.body[-1].x, self.body[-1].y, self.width, self.height))


    def check_collision(self, surface):
        screen_width, screen_height = surface.get_size()
        if self.head.collidelist(self.body) == -1 \
            and self.head.x >= 0 and self.head.x <= screen_width - self.width \
            and self.head.y >= 0 and self.head.y <= screen_height - self.height:
            return False
        return True 

    def draw_snake(self, surface):
        pg.draw.rect(surface, self.head_rgb, self.head)
        for segment in self.body:
            pg.draw.rect(surface, self.body_rgb, segment, width=1)

    def get_snake_coordinates(self):
        coordinates = []
        coordinates.append((self.head.x, self.head.y))
        for segment in self.body:
            coordinates.append((segment.x, segment.y))
        return coordinates

    def move(self):
        if self.direction == 'down':
            self.y_pos += self.velocity
        elif self.direction == 'up':
            self.y_pos -= self.velocity
        elif self.direction == 'right':
            self.x_pos += self.velocity
        elif self.direction == 'left':
            self.x_pos -= self.velocity
        if len(self.body) != 0:
            self.body.insert(0, pg.Rect(self.head.x, self.head.y, self.width, self.height))
            self.body.pop()
        self.head = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)  
        
    def update_direction(self, action):
        if len(self.previous_dirs) >= 4:
            self.previous_dirs.pop()
        if action == "down" and self.direction != 'up':
            self.direction = 'down'
            self.previous_dirs.append('down')
        elif action == "up" and self.direction != 'down':
            self.direction = 'up'
            self.previous_dirs.append('up')
        elif action == "right" and self.direction != 'left':
            self.direction = 'right'
            self.previous_dirs.append('right')
        elif action == "left" and self.direction != 'right':
            self.direction = 'left'
            self.previous_dirs.append('left')

class Food():
    def __init__(self, screen_width = 0, screen_height = 0):
        self.width = 10
        self.height = 10
        self.x_pos = 0
        self.y_pos = 0
        self.food_rgb = pg.Color(255, 0, 0)
        self.food = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def draw_food(self, surface):
        pg.draw.rect(surface, self.food_rgb, self.food)

    def is_eaten(self, snake_head):
        return self.food.colliderect(snake_head)

    def update_food_pos(self, surface, unavail_pos):
        screen_width, screen_height = surface.get_size()
        self.x_pos = random.randrange(0, screen_width - self.width, self.width)
        self.y_pos = random.randrange(0, screen_height - self.height, self.width)
        while (self.x_pos, self.y_pos) in unavail_pos:
            self.x_pos = random.randrange(0, screen_width - self.width, self.width)
            self.y_pos = random.randrange(0, screen_height - self.height, self.width)
        self.food = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)

class Snake_Game(Q_model):
    def __init__(self, width = 300, height = 300, rgb = [0, 0, 0]):
        self.width = width
        self.height = height
        self.rgb = rgb
        self.score = 0
        self.snake = Snake(self.width, self.height)
        self.food = Food(self.width, self.height)
        super().__init__(int(math.pow(2, 16)), 4)
        pg.init()
        self.window = pg.display.set_mode((self.width, self.height))
        self.window.fill(pg.Color(self.rgb[0],self.rgb[1], self.rgb[2]))
        pg.display.set_caption("SNAKE")
        pg.display.flip()

    def get_dir_state(self):
        if self.snake.direction == 'up':
            return [0,0]
        elif self.snake.direction == 'down':
            return [1,0]
        elif self.snake.direction == 'right':
            return [1,1]
        elif self.snake.direction == 'left':
            return [0,1]
        return [0,0]
        
    def get_food_pos_state(self):
        if self.food.y_pos < self.snake.head.y and self.food.x_pos < self.snake.head.x:
                #UL
                return [0,0,0]
        elif self.food.y_pos < self.snake.head.y and self.food.x_pos > self.snake.head.x:
                #UR
                return [1,0,0]
        elif self.food.y_pos > self.snake.head.y and self.food.x_pos < self.snake.head.x:
                #DL
                return [1,1,0]
        elif self.food.y_pos > self.snake.head.y and self.food.x_pos > self.snake.head.x:
                #DR
                return [1,1,1]
        elif self.food.y_pos < self.snake.head.y and self.food.x_pos == self.snake.head.x:
                #U-
                return [0,1,1]
        elif self.food.y_pos > self.snake.head.y and self.food.x_pos == self.snake.head.x:
                #D-
                return [0,0,1]
        elif self.food.y_pos == self.snake.head.y and self.food.x_pos < self.snake.head.x:
                #-L
                return [1,0,1]
        elif self.food.y_pos == self.snake.head.y and self.food.x_pos > self.snake.head.x:
                #-R
                return [0,1,0]
        return [0,0,0]

    def get_collision_state(self, snake_body):
        temp_state = [0,0,0,0]
        #CU
        if (self.snake.head.x, self.snake.head.y - self.snake.height) in snake_body[2:] or self.snake.head.y == 0:
            temp_state[0] = 1
        #CD
        if (self.snake.head.x, self.snake.head.y + self.snake.height) in snake_body[2:] or self.snake.head.y == self.height - self.snake.height:
            temp_state[1] = 1
        #CL
        if (self.snake.head.x - self.snake.width, self.snake.head.y) in snake_body[2:] or self.snake.head.x == 0:
            temp_state[2] = 1
        #CR
        if (self.snake.head.x + self.snake.width, self.snake.head.y) in snake_body[2:] or self.snake.head.x == self.width - self.snake.width:
            temp_state[3] = 1
        return temp_state

    def check_bounded(self, snake_body, coordinate, direction):
        #bounded Up, Down, Left, Right
        bounded = [False, False, False, False]
        if coordinate not in snake_body:
            if direction == "down":
                bounded[0] = True
            else:
                for temp_coordinate in snake_body:
                    if temp_coordinate[0] == coordinate[0] and temp_coordinate[1] < coordinate[1]:
                        bounded[0] = True
                        break
            if direction == "up":
                bounded[1] = True
            else:
                for temp_coordinate in snake_body:
                    if temp_coordinate[0] == coordinate[0] and temp_coordinate[1] > coordinate[1]:
                        bounded[1] = True
                        break
            if direction == "right":
                bounded[2] = True
            else:
                for temp_coordinate in snake_body:
                    if temp_coordinate[0] < coordinate[0] and temp_coordinate[1] == coordinate[1]:
                        bounded[2] = True
                        break
            if direction == "left":
                bounded[3] = True
            else:
                for temp_coordinate in snake_body:
                    if temp_coordinate[0] > coordinate[0] and temp_coordinate[1] == coordinate[1]:
                        bounded[3] = True
                        break
        if bounded == [True, True, True, True]:
            return True
        return False

    def check_loop_up(self, snake_body, collisions):
        coordinate = (self.snake.head.x, self.snake.head.y - self.snake.height)
        if self.snake.direction == "left" and collisions[2] == 1 or self.snake.direction == "right" and collisions[3] == 1:
            return self.check_bounded(snake_body, coordinate, "up")
        return False

    def check_loop_down(self, snake_body, collisions):
        coordinate = (self.snake.head.x, self.snake.head.y + self.snake.height)
        if  self.snake.direction == "left" and collisions[2] == 1 or self.snake.direction == "right" and collisions[3] == 1:
            return self.check_bounded(snake_body, coordinate, "down")
        return False

    def check_loop_left(self, snake_body, collisions):
        coordinate = (self.snake.head.x - self.snake.width, self.snake.head.y)
        if  self.snake.direction == "up" and collisions[0] == 1 or self.snake.direction == "down" and collisions[1] == 1:
            return self.check_bounded(snake_body, coordinate, "left")
        return False

    def check_loop_right(self, snake_body, collisions):
        coordinate = (self.snake.head.x + self.snake.width, self.snake.head.y)
        if  self.snake.direction == "up" and collisions[0] == 1 or self.snake.direction == "down" and collisions[1] == 1:
            return self.check_bounded(snake_body, coordinate, "right")
        return False


    def get_state(self, snake_body):
        state = []
        state += self.get_dir_state()
        state += self.get_food_pos_state()
        collisions = self.get_collision_state(snake_body)
        state += collisions
        if self.check_loop_up(snake_body, collisions):
            state.append(1)
        else:
            state.append(0)
        if self.check_loop_down(snake_body, collisions):
            state.append(1)
        else:
            state.append(0)
        if self.check_loop_left(snake_body, collisions):
            state.append(1)
        else:
            state.append(0)
        if self.check_loop_right(snake_body, collisions):
            state.append(1)
        else:
            state.append(0)
        
        return int(self.bin_state_to_num(state))

    def determine_reward(self, action, x_food_dist, y_food_dist, cur_dir, loop_values):
        if self.snake.check_collision(self.window):
            return -80
        if self.food.is_eaten(self.snake.head):
            return 40
        if cur_dir == "up" and action == "down" or cur_dir == "down" and action == "up" or cur_dir == "left" and action == "right" or cur_dir == "right" and action == "left":
            return -5
        if loop_values[0] and action == "up" or loop_values[1] and action == "down" or loop_values[2] and action == "left" or  loop_values[3] and action == "down":
            return -50
        if x_food_dist > abs(self.snake.head.x - self.food.x_pos) or y_food_dist > abs(self.snake.head.y - self.food.y_pos):
            return 1
        else:
            return -1
    
    def determine_dir(self, action):
        if action == 0:
            return "up"
        elif action == 1:
            return "down"
        elif action == 2:
            return "left"
        elif action == 3:
            return "right"

    def bin_state_to_num(self, state):
        state_num = 0
        index = 0
        for entry in state:
            state_num += entry * math.pow(2, index)
            index += 1
        return state_num

    def plot_reward_progress(self):
        self.episode_rewards.append(self.episode_rewards[-1] + self.episode_reward)
        plt.plot(self.episode_rewards)
        plt.ylabel("Rewards")
        plt.xlabel("Episode")
        plt.show(block = False)

        
    def play_game(self):
        self.food.update_food_pos(self.window, self.snake.get_snake_coordinates())
        figure, ax = plt.subplots(figsize = (4,5))
        plt.ion()
        # reward_plot, = ax.plot(self.episode_rewards)
        while True:
            if not self.snake.check_collision(self.window):
                self.update_window()
                event = pg.event.poll()
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                snake_body = self.snake.get_snake_coordinates()[1:]
                cur_dir = self.snake.direction
                cur_x_dist = abs(self.snake.head.x - self.food.x_pos)
                cur_y_dist = abs(self.snake.head.y - self.food.y_pos)
                collisions = self.get_collision_state(snake_body)  
                loop_values = [self.check_loop_up(snake_body, collisions), self.check_loop_down(snake_body, collisions), self.check_loop_left(snake_body, collisions), self.check_loop_right(snake_body, collisions)]
                state = self.get_state(snake_body)
                if self.check_explore():
                    action = random.randint(0,3)
                else:
                    action = self.best_action(state)
                self.snake.update_direction(self.determine_dir(action))
                self.snake.move()
                reward = self.determine_reward(action, cur_x_dist, cur_y_dist, cur_dir, loop_values)
                # self.episode_reward += reward
                new_state = self.get_state(snake_body)
                self.update_table(state, action, reward, new_state)
                self.epsilon *= 0.9999
                
                pg.time.wait(10)
            else:
                # reward_plot.set_ydata(self.episode_rewards.append(self.episode_rewards[-1] + self.episode_reward))
                # figure.canvas.draw()
                # figure.canvas.flush_events()
                # self.display_game_over()
                pg.time.wait(1000)
                self.reset_game()

    def reset_game(self):
        self.snake = Snake(self.width, self.height)
        self.food = Food(self.width, self.height)
        self.score = 0
        self.episode_reward = 0
        self.food.update_food_pos(self.window, self.snake.get_snake_coordinates())

    def update_window(self):
        self.window.fill(pg.Color(self.rgb[0], self.rgb[1], self.rgb[2]))
        if self.food.is_eaten(self.snake.head):
            self.food.update_food_pos(self.window, self.snake.get_snake_coordinates())
            self.snake.add_body()
            self.score += 1
        self.food.draw_food(self.window)
        self.snake.draw_snake(self.window)
        pg.display.flip()

if __name__ == "__main__":
    game = Snake_Game()
    game.play_game()