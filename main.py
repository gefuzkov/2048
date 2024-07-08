import pygame
from pygame.locals import *
from gamefunction import *

screen = pygame.display.set_mode((S_HEIGHT, S_WIDTH))
pygame.display.set_caption("2048")

def main():
    run = True
    board = Board()
    board.init_board()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_a:
                    board.move_board('left')
                elif event.key == K_d:
                    board.move_board('right')
                elif event.key == K_w:
                    board.move_board('up')
                elif event.key == K_s:
                    board.move_board('down')
                if event.key in (K_a, K_d, K_w, K_s):
                    board.spawn_cell()

        board.refresh()
        screen.fill(pygame.Color(BACKGROUND_COLOR_GAME))
        board.draw_board(screen)
        pygame.display.flip()

        if board.has_won():
            print("You win!")
            run = False
        if not board.can_move():
            print("Game Over!")
            run = False

    pygame.quit()

if __name__ == "__main__":
    main()

    
    
  