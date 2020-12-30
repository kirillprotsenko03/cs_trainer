import csv


FILENAME = 'statistic.csv'


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

      def write_statistic(self):
            data = (str(self.killed_ball),
                    str(self.miss),
                    str(self.scores))
            with open(FILENAME, 'a', newline='') as file:
                  writer = csv.writer(file)
                  writer.writerow(data)
                  print('data')
                        
                        
            

      def _create_file(self):
            with open(FILENAME, 'tw') as _:
                  None

