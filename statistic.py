import csv
from datetime import datetime


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

      def write_data(self):
            killed_ball = str(self.killed_ball)
            miss = str(self.miss)
            scores = str(self.scores)
            date = str(datetime.today())[:10]
            data = (date, scores, killed_ball, miss)
            with open(FILENAME, 'a', newline='') as file:
                  writer = csv.writer(file)
                  writer.writerow(data)
                        
      def _get_data(self) -> dict:
            data = {}
            with open(FILENAME, 'r') as file:
                  reader = csv.reader(file)
                  for row in reader:
                        date = row[0]
                        scores = row[1]
                        killed_ball = row[2]
                        miss = row[3]
                        if date not in data.keys():
                              data[date] = []
                        data[date].append((scores, killed_ball, miss))
                  return data
                  

