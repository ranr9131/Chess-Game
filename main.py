import pygame
from constants import *
from board import *
from Game import *

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Chess")

pygame.font.init()
WINNER_FONT = pygame.font.SysFont("arial",100)
def draw_winner(message):
    winner_text = WINNER_FONT.render(message,1,WHITE)
    WIN.blit(winner_text,((WIDTH//2)-(winner_text.get_width()//2),(HEIGHT//2)-(winner_text.get_height()//2)))
    pygame.display.update()
    pygame.time.delay(1000)

FPS = 60
def main():
    run = True
    clock = pygame.time.Clock()

    game = Game(WIN)


    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                game.select(*get_row_col_mouse(pygame.mouse.get_pos()))

        game.update()

        if game.winner() != None:
            winner_color_temp = None
            if game.winner() == BLACK:
                winner_color_temp = "Black"
            else:
                winner_color_temp = "White"
            draw_winner(f"{winner_color_temp} Won!")
            sep_run = True
            while sep_run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run,sep_run = False,False

    pygame.quit()


main()
