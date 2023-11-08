import numpy, random, threading, time


class Board:

  def __init__(self, size : tuple, cellSize : int):
    self.size = size
    self.cellSize = cellSize
    self.numMines = 99
    self.openCellList = []
    self.cellFlagged = []
    self.cellGameOver = ()
    self.grid = numpy.zeros(self.size)
    threading.Thread(target=self.reset).start()
    threading.Thread(target=self.random_mines).start()
  
  def get_grid(self):
    return self.grid
  
  def get_size(self):
    return self.size

  def reset(self):
    self.openCellList = []
    self.cellFlagged = []
    self.cellGameOver = []
    self.grid = numpy.zeros(self.size)
  
  def flag_all_cells(self):
    for i in range(0, self.size[0]):
      for j in range(0, self.size[1]): 
        if (i, j) not in self.cellFlagged:
          self.cellFlagged.append((i, j))

  def open_all_mine_cell(self):
    for i in range(0, self.size[0]):
      for j in range(0, self.size[1]): 
        if (i, j) not in self.openCellList and self.grid[i][j] == -1 and (i, j) not in self.cellFlagged:
          self.openCellList.append((i, j))
  
  def random_mines(self):
    mines = 0
    positions = [(i, j) for i in range(self.size[0]) for j in range(self.size[1])]
    random.shuffle(positions)
    while mines < self.numMines and positions:
        i, j = positions.pop()
        if self.grid[i][j] == 0:
            self.grid[i][j] = -1
            mines += 1
  
  def count_mines(self):
    for row in range(self.size[0]):
      for col in range(self.size[1]):
        if self.grid[row][col] != -1:
          count = 0
          for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
              if i >= 0 and i < len(self.grid) and j >= 0 and j < len(self.grid[i]) and self.grid[i][j] == -1:
                count += 1
          self.grid[row][col] = count
