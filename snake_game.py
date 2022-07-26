import pygame as pg
import random

class Snake():
    def __init__(self, screen_width = 0, screen_height = 0):
        self.x_pos = screen_width/2
        self.y_pos = screen_height/2
        self.width = 10
        self.height = 10
        self.velocity = 10
        self.direction = 'stop'
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

    def get_snake_cordinates(self):
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
        

    def update_direction(self, event):
        if event.key == pg.K_DOWN and self.direction != 'up':
            self.direction = 'down'
        elif event.key == pg.K_UP and self.direction != 'down':
            self.direction = 'up'
        elif event.key == pg.K_RIGHT and self.direction != 'left':
            self.direction = 'right'
        elif event.key == pg.K_LEFT and self.direction != 'right':
            self.direction = 'left'

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

class Snake_Game():
    def __init__(self, width = 300, height = 300, rgb = [0, 0, 0]):
        self.width = width
        self.height = height
        self.rgb = rgb
        self.score = 0
        self.snake = Snake(self.width, self.height)
        self.food = Food(self.width, self.height)
        pg.init()
        self.window = pg.display.set_mode((self.width, self.height))
        self.window.fill(pg.Color(self.rgb[0],self.rgb[1], self.rgb[2]))
        pg.display.set_caption("SNAKE")
        pg.display.flip()

    def display_game_over(self):
        offset = -20
        game_over_font = pg.font.SysFont('arial', 30)
        game_over_txt = game_over_font.render('GAME OVER', True, (255, 0, 0), (0, 0, 0))
        self.window.blit(game_over_txt, ((self.window.get_width() / 2 - game_over_txt.get_width() / 2), 
            (self.window.get_height() / 2) - game_over_txt.get_height() + offset))
        score_font = pg.font.SysFont('arial', 25)
        score_txt = score_font.render('Score: ' + str(self.score), True, (255, 0, 0), (0, 0, 0))
        self.window.blit(score_txt, ((self.window.get_width() / 2 - score_txt.get_width() / 2), 
            (self.window.get_height() / 2) - score_txt.get_height() + game_over_txt.get_height() + offset))
        restart_font = pg.font.SysFont('arial', 15)
        restart_txt = restart_font.render('Press Any Key To Restart', True, (255, 0, 0), (0, 0, 0))
        self.window.blit(restart_txt, ((self.window.get_width() / 2 - restart_txt.get_width() / 2), 
            (self.window.get_height() / 2) - restart_txt.get_height() + game_over_txt.get_height() + score_txt.get_height() +offset))
        pg.display.flip()
    
    def play_game(self):
        self.food.update_food_pos(self.window, self.snake.get_snake_cordinates())
        while True:
            if not self.snake.check_collision(self.window):
                self.update_window()
                print(self.snake.head.x, self.snake.head.y)
                event = pg.event.poll()
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    self.snake.update_direction(event)
                self.snake.move()
                pg.time.wait(100)
            else:
                self.display_game_over()
                event = pg.event.poll()
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    self.reset_game()

    def reset_game(self):
        self.snake = Snake(self.width, self.height)
        self.food = Food(self.width, self.height)
        self.score = 0
        self.food.update_food_pos(self.window, self.snake.get_snake_cordinates())

    def update_window(self):
        self.window.fill(pg.Color(self.rgb[0],self.rgb[1], self.rgb[2]))
        if self.food.is_eaten(self.snake.head):
            self.food.update_food_pos(self.window, self.snake.get_snake_cordinates())
            self.snake.add_body()
            self.score += 1
        self.food.draw_food(self.window)
        self.snake.draw_snake(self.window)
        pg.display.flip()

if __name__ == "__main__":
    game = Snake_Game()
    game.play_game()