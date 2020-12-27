import pygame
import sys
import random
import time



#  GLOBAL VARIABLES
X = 600  # width of screen
Y = 600  # height of screen
SCREEN_COLOR = (0, 0, 0)
RED = (255, 0, 0)
GAME_NAME = 'CS-TRAINER'
FPS = 5


class Ball:
      def __init__(self, radius=20):
            self.radius = radius
            self.x = random.randint(0, X)
            self.y = random.randint(0, Y)

      def draw(self, screen):
            pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

      def is_click_in_ball(self, pos: tuple) -> bool:
            click_x = pos[0]
            click_y = pos[1]
            is_x = (self.x - self.radius) <= click_x <= (self.x + self.radius)
            is_y = self.y - self.radius <= click_y <= self.y + self.radius
            if is_x and is_y:
                  return True
            return False

      def make_less_radius(self, decrease: int):
            self.radius -= decrease  # decrease depends on level of game

      def is_need_del(self) -> bool:
            if self.radius <= 2:
                  return True
            return False


class Level:
      def __init__(self, ball_list):
            self.difficult = 1
            self.ball_list = ball_list
            self.addiction_ball_time = time.time()

      def make_balls_less(self):
            for ball in self.ball_list:
                  ball.make_less_radius(self.difficult)
                  self._del_unnecessary_balls(ball)  # del balls witch radius is less than two

      def add_ball_to_game(self):
            global Ball
            if  time.time() - self.addiction_ball_time >= 1:
                  self.ball_list.append(Ball())
                  self.addiction_ball_time = time.time()

      def get_difficult(self) -> int:
            return self.difficult

      def _del_unnecessary_balls(self, ball):
            if ball.is_need_del():
                  self.ball_list.remove(ball)

class GameStatistic:
      def __init__(self):
            """ count score of player, killed ball and miss.
                  write statistic to csv file and show diagrams"""
            self.killed_ball = 0
            self.miss = 0
            self.scores = 0

      def add_score(self, difficult):
            self.killed_ball += 1
            self.scores += 100 * difficult

      def del_score(self):
            self.miss += 1
            if self.scores >= 100:
                  self.scores -= 50

      def show(self):
            pass


class MenuButton:
      def __init__(self):
            self.lenght = 100
            self.height = 50
            self.x = X // 2 - self.lenght // 2
            self.y = Y // 2 - self.height // 2

      def draw(self, screen):
            pygame.draw.rect(screen, RED, (self.x, self.y, self.lenght, self.height))

      def is_click_in_button(self, mouse_pos: tuple) -> bool:
            mouse_x = mouse_pos[0]
            mouse_y = mouse_pos[1]

            if self.x <= mouse_x <= self.x + self.lenght and self.y <= mouse_y <= self.y + self.height:
                  return True
            return False


class Game:
      def __init__(self, Ball, Level, GameStatistic, MenuButton):
            self.clock = pygame.time.Clock()
            pygame.init()
            self.screen = pygame.display.set_mode((X, Y))
            pygame.display.set_caption(GAME_NAME)
            self.statistic = GameStatistic()
            self.status = 'menu'
            self.start_button = MenuButton()
            

      def check_events(self):
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        sys.exit()
                  elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if game.status == 'play':
                              self._handle_game_event(mouse_pos)
                        elif game.status == 'menu':
                              self._handle_menu_event(mouse_pos)

      def _handle_menu_event(self, mouse_pos):
            get_in = False
            if self.start_button.is_click_in_button(mouse_pos):
                  self._start_play()
                        

      def _handle_game_event(self, mouse_pos):
                  get_in = False  # if player not get in target: False, else: True
                  for ball in self.ball_list:
                        if ball.is_click_in_ball(mouse_pos):
                              self.ball_list.remove(ball)
                              difficult = self.level.get_difficult()
                              self.statistic.add_score(difficult)
                              get_in = True
                              break
                  if not get_in:
                        self.statistic.del_score()

      def _start_play(self):
            self.start_play_time = time.time()
            self.ball_list = [Ball()]  # list of all balls on screen at the moment of game
            self.level = Level(self.ball_list)
            self.status = 'play'

      def _stop_play(self):
            del self.ball_list
            del self.level
            self.status = 'menu'
            self.statistic.__init__()
            

      def draw(self):
            self.screen.fill(SCREEN_COLOR)
            if self.status == 'play':
                  for ball in self.ball_list:
                        ball.draw(self.screen)
            elif self.status == 'menu':
                  self.start_button.draw(self.screen)
                        
            pygame.display.flip()


      def main(self):
            while True:
                  self.clock.tick(FPS)
                  if self.status == 'play':
                        self.level.make_balls_less()
                        self.level.add_ball_to_game()
                        if time.time() - self.start_play_time >= 60:  # 60 is one min in sec
                              self._stop_play()
                              
                  self.check_events()
                  self.draw()
            

if __name__ == '__main__':
      game = Game(Ball, Level, GameStatistic, MenuButton)
      game.main()
