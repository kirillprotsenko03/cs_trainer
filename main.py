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
      def __init__(self, screen, radius=20):
            self.screen = screen
            self.radius = radius
            self.x = random.randint(0, X)
            self.y = random.randint(0, Y)

      def draw(self):
            pygame.draw.circle(self.screen, RED, (self.x, self.y), self.radius)

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

      def add_ball_to_game(self, screen):
            global Ball
            if  time.time() - self.addiction_ball_time >= 1:
                  self.ball_list.append(Ball(screen))
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
            self.score = 0

      def add_score(self, difficult):
            self.killed_ball += 1
            self.score += 100 * difficult

      def del_score(self):
            self.miss += 1
            if self.score >= 100:
                  self.score -= 50

      def show(self):
            pass


class Game:
      def __init__(self, Ball, Level, GameStatistic):
            self.clock = pygame.time.Clock()
            pygame.init()
            self.screen = pygame.display.set_mode((X, Y))
            pygame.display.set_caption(GAME_NAME)
            self.ball_list = [Ball(self.screen)]  # list of all balls on screen at the moment of game
            self.level = Level(self.ball_list)
            self.statistic = GameStatistic()

      def check_events(self):
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        sys.exit()
                  if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
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


      def draw(self):
            self.screen.fill(SCREEN_COLOR)
            for ball in self.ball_list:
                  ball.draw()
            pygame.display.flip()


      def main(self):
            while True:
                  self.clock.tick(FPS)
                  self.level.make_balls_less()
                  self.level.add_ball_to_game(self.screen)
                  self.check_events()
                  self.draw()
            

if __name__ == '__main__':
      game = Game(Ball, Level, GameStatistic)
      game.main()
