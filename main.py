import pygame as pg
import sys
from Scripts.game import *
from Scripts.board import *


class Main:

  def __init__(self) -> None:
    pg.init()
    cellSize = 30
    gridSize = (30, 16)
    self.display = pg.display.set_mode((
      cellSize * gridSize[0] + 20 * 2,
      cellSize * gridSize[1] + 115
    ))
    self.clock = pg.time.Clock()
    self.board = Board(gridSize, cellSize)
    self.game = Game(self.display, self.board)
    pg.display.set_icon(pg.image.load("Assets/Icon.png"))
    pg.display.set_caption("Minesweeper")

  def check_event(self):
    for e in pg.event.get():
      if e.type == pg.QUIT:
        pg.quit()
        sys.exit()
      self.game.handl(e)
  
  def draw(self):
    self.display.fill([192] * 3)
    self.game.draw()
  
  def update(self):
    pg.display.update()
    pg.display.set_caption(f"Minesweeper | Fps:{self.clock.get_fps():.1f}")
    self.game.update()
    self.clock.tick(60)
  
  def run(self):
    while True:
      self.draw()
      self.check_event()
      self.update()


if __name__ == "__main__":
  main = Main()
  main.run()
