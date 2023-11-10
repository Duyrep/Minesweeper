import pygame as pg
import os, typing, time, threading
from Scripts.board import *


class Game:

  def __init__(
    self,
    display : pg.Surface,
    board : Board
  ):
    self.display = display
    self.board = board
    self.mousePos = pg.mouse.get_pos()
    self.displaySize = display.get_size()
    self.imageCell = self.load_image_cell()
    self.imageFace = self.load_image_face()
    self.imageNumber = self.load_image_number()
    self.imageBorder = self.load_image_border()
    self.click = True
    self.faceStatus = "SmileyFace"
    self.gameover = False
    self.win = False
    self.rectcol = False
    self.start_ticks = 0.0
    self.timer = 0.0
    self.misflaggedMineCell = []
    self.mouseDownPosOnGrid = (0, 0)
    self.mousePosPressed = []
  
  def load_image_cell(self):
    image = {}
    for file in os.listdir("Assets"):
      if file.endswith(".png"):
        if "Cell" in file:
          image[file[:-4]] = pg.image.load(f"Assets/{file}")
    return image

  def load_image_face(self):
    image = {}
    for file in os.listdir("Assets"):
      if file.endswith(".png"):
        if "Face" in file:
          image[file[:-4]] = pg.image.load(f"Assets/{file}")
    return image

  def load_image_number(self):
    image = {}
    for file in os.listdir("Assets"):
      if file.endswith(".png"):
        if "Number" in file:
          image[file[:-4]] = pg.image.load(f"Assets/{file}")
    return image
  
  def load_image_border(self):
    image = {}
    for file in os.listdir("Assets"):
      if file.endswith(".png"):
        if "Border" in file:
          image[file[:-4]] = pg.image.load(f"Assets/{file}")
    return image

  def handl(self, event : typing.List[pg.event.Event]):
    mousePressed = pg.mouse.get_pressed()
    if \
      0 < (self.mousePos[0] - 20) / self.board.cellSize < self.board.size[0] and \
      0 < (self.mousePos[1] - 95) / self.board.cellSize < self.board.size[1]:
      mousePosOnGrid = (
        int((self.mousePos[0] - 20) / self.board.cellSize),
        int((self.mousePos[1] - 95) / self.board.cellSize)
      )
      if mousePressed[0]:
        self.mousePosPressed = mousePosOnGrid
      else:
        self.mousePosPressed = ()
      if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 1:
          self.mouseDownPosOnGrid = mousePosOnGrid
          self.faceStatus = "ScaredFace"
          if self.gameover and not self.win:
            self.faceStatus = "SadFace"
          if self.gameover and self.win:
            self.faceStatus = "CoolFace"
      elif event.type == pg.MOUSEBUTTONUP:
        if event.button == 1:
          if mousePosOnGrid == self.mouseDownPosOnGrid and not self.gameover:
            if mousePosOnGrid not in self.board.openCellList and mousePosOnGrid not in self.board.cellFlagged:
              if self.board.grid[mousePosOnGrid[0]][mousePosOnGrid[1]] != -1:
                if self.click:
                  threading.Thread(target=self.board.count_mines()).start()
                  self.click = False
                  self.start_ticks = pg.time.get_ticks()
                threading.Thread(target=self.automatically_open_cells, args=(mousePosOnGrid[0], mousePosOnGrid[1])).start()
              elif self.click:
                if self.board.grid[mousePosOnGrid[0]][mousePosOnGrid[1]] == -1:
                  a = False
                  self.board.grid[mousePosOnGrid[0]][mousePosOnGrid[1]] = 0
                  for i in range(self.board.size[0]):
                    for j in range(self.board.size[1]):
                      if self.board.grid[i][j] == 0:
                        self.board.grid[i][j] = -1
                        threading.Thread(target=self.automatically_open_cells, args=(mousePosOnGrid[0], mousePosOnGrid[1])).start()
                        a = True
                        break
                    if a:
                      break
                threading.Thread(target=self.board.count_mines()).start()
                self.start_ticks = pg.time.get_ticks()
                self.click = False
              else:
                self.gameover = True
                self.faceStatus = "SadFace"
                self.board.cellGameOver = (mousePosOnGrid[0], mousePosOnGrid[1])
                threading.Thread(target=self.board.open_all_mine_cell).start()
        elif event.button == 3 and not self.gameover:
          if mousePosOnGrid not in self.board.cellFlagged and mousePosOnGrid not in self.board.openCellList:
            self.board.cellFlagged.append(mousePosOnGrid)
          elif mousePosOnGrid not in self.board.openCellList:
            self.board.cellFlagged.remove(mousePosOnGrid)
          if mousePosOnGrid not in self.misflaggedMineCell and \
            self.board.grid[mousePosOnGrid[0]][mousePosOnGrid[1]] != -1:
            self.misflaggedMineCell.append(mousePosOnGrid)
          elif mousePosOnGrid in self.misflaggedMineCell:
            self.misflaggedMineCell.remove(mousePosOnGrid)
      elif event.type == pg.KEYDOWN:
        if event.key == pg.K_r:
          self.gameover = False
          self.faceStatus = "SmileyFace"
          threading.Thread(target=self.board.reset).start()
          threading.Thread(target=self.board.random_mines).start()

    rect1 = pg.Rect(self.displaySize[0] / 2 - 20, 28, 40, 40)
    if event.type == pg.MOUSEBUTTONDOWN:
      if event.button == 1 and rect1.collidepoint(pg.mouse.get_pos()):
        self.faceStatus = "PressedSmileyFace"
        self.rectcol = rect1.collidepoint(pg.mouse.get_pos())
    elif event.type == pg.MOUSEBUTTONUP:
      if event.button == 1:
        self.faceStatus = "SmileyFace"
        if self.gameover:
          self.faceStatus = "SadFace"
        if self.gameover and self.win:
          self.faceStatus = "CoolFace"
        if rect1.collidepoint(pg.mouse.get_pos()) and self.rectcol:
          self.misflaggedMineCell = []
          self.win = False
          self.click = True
          self.gameover = False
          self.start_ticks = pg.time.get_ticks()
          self.timer = (pg.time.get_ticks() - self.start_ticks) / 1000
          self.faceStatus = "SmileyFace"
          threading.Thread(target=self.board.reset).start()
          threading.Thread(target=self.board.random_mines).start()
        self.rectcol = False
          
  def automatically_open_cells(self, row, col):
    cell_nextopen = []
    self.board.openCellList.append((row, col))
    if self.board.grid[row][col] == 0:
      for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
          if i >= 0 and i < len(self.board.grid) and j >= 0 and j < len(self.board.grid[i]) and self.board.grid[i][j] >= 0:
            if (i, j) not in self.board.openCellList and (i, j) not in self.board.cellFlagged:
              self.board.openCellList.append((i, j))
              if self.board.grid[i][j] == 0:
                cell_nextopen.append((i, j))
    for cell in cell_nextopen:
      row, col = cell
      for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
          if i >= 0 and i < len(self.board.grid) and j >= 0 and j < len(self.board.grid[i]) and self.board.grid[i][j] >= 0:
            if (i, j) not in self.board.openCellList and (i, j) not in self.board.cellFlagged:
              self.board.openCellList.append((i, j))
              if self.board.grid[i][j] == 0 and (i, j) not in cell_nextopen:
                cell_nextopen.append((i, j))
    self.checkwin()
  
  def checkwin(self):
    self.gameover = len(self.board.openCellList) == self.board.size[0] * self.board.size[1] - self.board.numMines
    self.win = len(self.board.openCellList) == self.board.size[0] * self.board.size[1] - self.board.numMines
    if self.win:
      self.faceStatus = "CoolFace"
      self.board.flag_all_cells()

  def draw_grid(self):
    mousePressed = pg.mouse.get_pressed()
    surface = pg.Surface((self.board.cellSize * self.board.size[0], self.board.cellSize * self.board.size[1]))
    surface.fill((192, 192, 192))
    surfaceCellSize = [self.board.cellSize] * 2
    for i in range(self.board.size[0]):
      for j in range(self.board.size[1]):
        pos = (i * self.board.cellSize, j * self.board.cellSize)
        cell = (i, j)
        if cell in self.board.openCellList:
          cell_type = "ExplodedMineCell" if cell == self.board.cellGameOver else \
                      f"Cell{int(self.board.grid[i][j])}" if self.board.grid[i][j] > 0 else \
                      "UntriggeredMineCell" if self.board.grid[i][j] == -1 else \
                      "EmptyCell"
        elif self.gameover and cell in self.misflaggedMineCell:
          cell_type = "MisflaggedMineCell"
        elif cell in self.board.cellFlagged:
          cell_type = "FlaggedCell"
        elif cell == self.mousePosPressed and mousePressed[0] and not self.gameover:
          cell_type = "EmptyCell"
        else:
          cell_type = "HiddenCell"
        surface.blit(pg.transform.scale(self.imageCell[cell_type], surfaceCellSize), pos)
    self.display.blit(surface, (20, self.displaySize[1] - 20 - self.board.cellSize * self.board.size[1]))

  
  def draw_face(self):
    self.display.blit(pg.transform.scale(self.imageFace[self.faceStatus], (40, 40)), (self.displaySize[0] / 2 - 20, 28))
  
  def draw_number(self):
    flagNumSurface = pg.Surface((60, 40))
    flagNum = str(self.board.numMines - len(self.board.cellFlagged)).zfill(3)
    if int(flagNum) < 0:
      flagNum = "000"
    for i in range(3):
      flagNumSurface.blit(pg.transform.scale(self.imageNumber[f"Number{flagNum[i]}"], (20, 40)), (i*20, 0))
    self.display.blit(flagNumSurface, (28, 28))

    timerSurface = pg.Surface((60, 40))
    timer = str(int(self.timer)).zfill(3)
    if len(timer) > 3:
      timer = "999"
    for i in range(3):
      timerSurface.blit(pg.transform.scale(self.imageNumber[f"Number{timer[i]}"], (20, 40)), (i*20, 0))
    self.display.blit(timerSurface, (self.displaySize[0] - 90, 30))
  
  def draw_border(self):
    w = (self.displaySize[0], 20)
    h = (20, self.displaySize[1])
    self.display.blit(pg.transform.scale(self.imageBorder["BorderHeight"], h), (0, 20))
    self.display.blit(pg.transform.scale(self.imageBorder["BorderHeight"], h), (self.displaySize[0] - 20, 20))
    self.display.blit(pg.transform.scale(self.imageBorder["BorderWidth"], w), (20, 0))
    self.display.blit(pg.transform.scale(self.imageBorder["BorderWidth"], w), (20, self.displaySize[1] - 20))
    self.display.blit(pg.transform.scale(self.imageBorder["BorderWidth"], w), (20, 75))
    self.display.blit(self.imageBorder["Upper-leftCornerBorder"], (0, 0))
    self.display.blit(self.imageBorder["Upper-rightCornerBorder"], (self.displaySize[0] - 20, 0))
    self.display.blit(self.imageBorder["BottomLeftCornerBorder"], (0, self.displaySize[1] - 20))
    self.display.blit(self.imageBorder["BottomRightCornerBorder"], (self.displaySize[0] - 20, self.displaySize[1] - 20))
    self.display.blit(pg.transform.scale(self.imageBorder["LeftBarCornerBorder"], (20, 20)), (0, 75))
    self.display.blit(pg.transform.scale(self.imageBorder["RightBarCornerBorder"], (20, 20)), (self.displaySize[0] - 20, 75))

  def draw(self):
    self.draw_grid()
    self.draw_face()
    self.draw_number()
    self.draw_border()

  def update(self):
    if not self.click and not self.gameover:
      self.timer = (pg.time.get_ticks() - self.start_ticks) / 1000
    self.displaySize = self.display.get_size()
    self.mousePos = pg.mouse.get_pos()