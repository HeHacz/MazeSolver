from cell import Cell
import time, random

class Maze: 
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        if seed:
            random.seed(seed) 

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
        
    def _create_cells(self):
        for x in range(0, self.num_cols):
            cells = []
            for y in range(0, self.num_rows):
                cells.append(Cell(self.win))
            self._cells.append(cells)
        for x in range(0, self.num_cols):
            for y in range(0, self.num_rows):
                self._draw_cell(x, y)
        
    
    def _draw_cell(self, x, y):
        if not self.win:
            return
        x1 = self.x1 + x * self.cell_size_x
        y1 = self.y1 + y * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self._cells[x][y].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if not self.win:
            return
        self.win.redraw()
        time.sleep(0.03)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, x, y):
        self._cells[x][y].visited = True
        while True:
            adjecent_cells = []

            if x > 0 and not self._cells[x - 1][y].visited:
                adjecent_cells.append((x - 1, y))
            if x < self.num_cols - 1 and not self._cells[x + 1][y].visited:
                adjecent_cells.append((x + 1, y))
            if y > 0 and not self._cells[x][y - 1].visited:
                adjecent_cells.append((x, y - 1))
            if y < self.num_rows - 1 and not self._cells[x][y + 1].visited:
                adjecent_cells.append((x, y + 1))

            if not adjecent_cells:
                self._draw_cell(x, y)
                return
            
            destination = random.randrange(len(adjecent_cells))
            destination_index = adjecent_cells[destination]
            
            if destination_index[0] == x - 1:
                self._cells[x][y].has_left_wall = False
                self._cells[x - 1][y].has_right_wall = False
            
            if destination_index[0] == x + 1:
                self._cells[x][y].has_right_wall = False
                self._cells[x + 1][y].has_left_wall = False

            if destination_index[1] == y + 1:
                self._cells[x][y].has_bottom_wall = False
                self._cells[x][y + 1].has_top_wall = False

            if destination_index[1] == y - 1:
                self._cells[x][y].has_top_wall = False
                self._cells[x][y - 1].has_bottom_wall = False

            self._break_walls_r(destination_index[0], destination_index[1])

    def _reset_cells_visited(self):
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                self._cells[x][y].visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, x, y):
        self._animate()
        self._cells[x][y].visited = True

        if x == self.num_cols - 1 and y == self.num_rows - 1:
            return True
        
        #left
        if x > 0 and not self._cells[x][y].has_left_wall and not self._cells[x - 1][y].visited:
            self._cells[x][y].draw_move(self._cells[x - 1][y])
            if self._solve_r(x - 1, y):
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x - 1][y], True)

        #right
        if x < self.num_cols - 1 and not self._cells[x][y].has_right_wall and not self._cells[x + 1][y].visited:
            self._cells[x][y].draw_move(self._cells[x + 1][y])

            if self._solve_r(x + 1, y):
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x + 1][y], True)
        # up
        if y > 0 and not self._cells[x][y].has_top_wall and not self._cells[x][y - 1].visited:
            self._cells[x][y].draw_move(self._cells[x][y - 1])
            if self._solve_r(x, y - 1):
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x][y - 1], True)
        if y < self.num_rows and not self._cells[x][y].has_bottom_wall and not self._cells[x][y + 1].visited:
            self._cells[x][y].draw_move(self._cells[x][y + 1])
            if self._solve_r(x, y + 1):
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x][y + 1], True)

        return False