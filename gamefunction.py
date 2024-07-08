import random
import pygame
from pygame.locals import *

S_HEIGHT = 600 + 125
S_WIDTH = 600 + 125 + 50
BOARD_HEIGHT = 4
BOARD_WIDTH = 4
BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 
                         4: "#ede0c8", 
                         8: "#f2b179",
                         16: "#f59563", 
                         32: "#f67c5f", 
                         64: "#f65e3b",
                         128: "#edcf72", 
                         256: "#edcc61", 
                         512: "#edc850",
                         1024: "#edc53f", 
                         2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 
                   4: "#776e65", 
                   8: "#f9f6f2", 
                   16: "#f9f6f2",
                   32: "#f9f6f2", 
                   64: "#f9f6f2", 
                   128: "#f9f6f2",
                   256: "#f9f6f2", 
                   512: "#f9f6f2", 
                   1024: "#f9f6f2",
                   2048: "#f9f6f2"}
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("DejaVu Sans Mono Nerd Font Mono", 52, True)

class Cell:
    def __init__(self, rect, value):
        self.rect = rect
        self.value = value
        self.refresh_colors()

    def refresh_colors(self):
        if self.value:
            self.fg = pygame.Color(CELL_COLOR_DICT[self.value])
            self.bg = pygame.Color(BACKGROUND_COLOR_DICT[self.value])
        else:
            self.fg = ""
            self.bg = pygame.Color(BACKGROUND_COLOR_CELL_EMPTY)

class Board:
    def __init__(self):
        self._board = [[Cell("", 0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0

    def init_board(self):
        left_offset = 25
        top_offset = 25
        for h in range(BOARD_HEIGHT):
            for w in range(BOARD_WIDTH):
                self._board[h][w].rect = pygame.Rect((left_offset * h + (h * 150)) + 25,
                                                     (top_offset * w + (w * 150)) + 25, 150, 150)
        for _ in range(2):
            self.spawn_cell()

    def spawn_cell(self):
        empty_cells = [(h, w) for h in range(BOARD_HEIGHT) for w in range(BOARD_WIDTH) if self._board[h][w].value == 0]
        if empty_cells:
            h, w = random.choice(empty_cells)
            self._board[h][w].value = random.choices([2, 4], weights=[0.85, 0.15])[0]
    
    def draw_board(self, screen):
        global font
        for row in self._board:
            for cell in row:
                pygame.draw.rect(screen, cell.bg, cell.rect)
                if cell.value != 0:
                    value_label = font.render(str(cell.value), True, cell.fg)
                    screen.blit(value_label, ((cell.rect.left + 72) - 13 * len(str(cell.value)), cell.rect.top + 50))

        score_font = pygame.font.SysFont("Verdana", 30, True)
        score_label = score_font.render("Score:   " + str(self.score), True, (0, 0, 0))
        screen.blit(score_label, (S_WIDTH / 12, 717))
        self.score = sum(cell.value for row in self._board for cell in row)

    def move_board(self, direction):
        if direction == 'left':
            for row in self._board:
                self._move_row_left(row)
        elif direction == 'right':
            for row in self._board:
                self._move_row_right(row)
        elif direction == 'up':
            for col in range(BOARD_WIDTH):
                self._move_column_up(col)
        elif direction == 'down':
            for col in range(BOARD_WIDTH):
                self._move_column_down(col)

    def _move_row_left(self, row):
        merged = [False] * BOARD_WIDTH
        for i in range(1, BOARD_WIDTH):
            if row[i].value != 0:
                j = i
                while j > 0 and row[j - 1].value == 0:
                    row[j - 1].value = row[j].value
                    row[j].value = 0
                    j -= 1
                if j > 0 and row[j - 1].value == row[j].value and not merged[j - 1]:
                    row[j - 1].value *= 2
                    row[j].value = 0
                    merged[j - 1] = True

    def _move_row_right(self, row):
        merged = [False] * BOARD_WIDTH
        for i in range(BOARD_WIDTH - 2, -1, -1):
            if row[i].value != 0:
                j = i
                while j < BOARD_WIDTH - 1 and row[j + 1].value == 0:
                    row[j + 1].value = row[j].value
                    row[j].value = 0
                    j += 1
                if j < BOARD_WIDTH - 1 and row[j + 1].value == row[j].value and not merged[j + 1]:
                    row[j + 1].value *= 2
                    row[j].value = 0
                    merged[j + 1] = True

    def _move_column_up(self, col):
        merged = [False] * BOARD_HEIGHT
        for i in range(1, BOARD_HEIGHT):
            if self._board[i][col].value != 0:
                j = i
                while j > 0 and self._board[j - 1][col].value == 0:
                    self._board[j - 1][col].value = self._board[j][col].value
                    self._board[j][col].value = 0
                    j -= 1
                if j > 0 and self._board[j - 1][col].value == self._board[j][col].value and not merged[j - 1]:
                    self._board[j - 1][col].value *= 2
                    self._board[j][col].value = 0
                    merged[j - 1] = True

    def _move_column_down(self, col):
        merged = [False] * BOARD_HEIGHT
        for i in range(BOARD_HEIGHT - 2, -1, -1):
            if self._board[i][col].value != 0:
                j = i
                while j < BOARD_HEIGHT - 1 and self._board[j + 1][col].value == 0:
                    self._board[j + 1][col].value = self._board[j][col].value
                    self._board[j][col].value = 0
                    j += 1
                if j < BOARD_HEIGHT - 1 and self._board[j + 1][col].value == self._board[j][col].value and not merged[j + 1]:
                    self._board[j + 1][col].value *= 2
                    self._board[j][col].value = 0
                    merged[j + 1] = True

    def refresh(self):
        for row in self._board:
            for cell in row:
                cell.refresh_colors()

    def can_move(self):
        for row in self._board:
            for cell in row:
                if cell.value == 0:
                    return True
        for row in self._board:
            for i in range(BOARD_WIDTH - 1):
                if row[i].value == row[i + 1].value:
                    return True
        for col in range(BOARD_WIDTH):
            for i in range(BOARD_HEIGHT - 1):
                if self._board[i][col].value == self._board[i + 1][col].value:
                    return True
        return False

    def has_won(self):
        return any(cell.value == 2048 for row in self._board for cell in row)



