# from lib.board_cy import Board as Board_cy
from lib.board import Board
# from lib.node import Node
from res.glob import *
from time import time
import pygame


def main():
    pygame.display.init()
    pygame.display.set_caption(TITLE)
    
    scrSize = (WIDTH + 1, HEIGHT + 1) if DRAW_GRID else (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(scrSize)
    
    board = Board(screen, (WIDTH, HEIGHT), PIXEL_NUM, 
                  draw_grid=DRAW_GRID, map=MAP, animations=ANIMATIONS)
    
    # board = Board_cy(screen, (WIDTH, HEIGHT), PIXEL_NUM, 
    #                  draw_grid=DRAW_GRID, map=MAP, animations=ANIMATIONS)
    
    isAlgorithmStarted = False

    while True:
        if (rv := runTime(board, isAlgorithmStarted)):
            if rv == 2:
                if not board.startAlgorithm(lambda: runTime(board, True)):
                    break
        else:
            break
    
    pygame.quit()


def runTime(board, isAlgorithmStarted):
    startTime = time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (board.startNodePos and board.endNodePos):
                # isAlgorithmStarted = bool(1) # Düştüm
                # isAlgorithmStarted = True
                # board.startAlgorithm(lambda: update(board, startTime, FPS))
                return 2
                
        if isAlgorithmStarted:
            continue
                    
        if pygame.mouse.get_pressed()[0]:
            pos = board.getClickedPos(pygame.mouse.get_pos())
            if board.getNodeState(pos) == states.empty:
                if not board.startNodePos:
                    board.setNodeState(pos, states.start)
                elif not board.endNodePos:
                    board.setNodeState(pos, states.end)
                else:
                    board.setNodeState(pos, states.wall)

        elif pygame.mouse.get_pressed()[2]:
            pos = board.getClickedPos(pygame.mouse.get_pos())
            board.setNodeState(pos, states.empty)


    update(board, startTime, FPS)
    return 1


def update(board, startTime, fps):
    board.update()
    pygame.display.update()
    while time() - startTime < (1 / fps):
        pass


if __name__ == "__main__":
    main()