import time
import pygame

from ai import ai_algorithm
from checkers.game import Game
from constants import DARK, SCREEN_WIDTH, SCREEN_HEIGHT, LIGHT, BOARD_DARK, WHITE
from utilities.button import Button


def draw_text(screen, text, font, colour, coordinates):
    text_img = font.render(text, True, colour)
    screen.blit(text_img, coordinates)


def draw_text_center(screen, text, font, colour, y):
    text_img = font.render(text, True, colour)
    x = SCREEN_WIDTH / 2 - text_img.get_width() / 2
    screen.blit(text_img, (x, y))


def draw_turn_text(screen, game, text_font, text_colour):
    small_surface = pygame.Surface((150, 100))
    small_surface.fill((50, 75, 105))
    if game.current_turn is DARK:
        draw_text(small_surface, "Dark AI Turn", text_font, text_colour, (0, 0))
    else:
        draw_text(small_surface, "Light AI Turn", text_font, text_colour, (0, 0))
    turn_text_x = SCREEN_WIDTH / 2 - small_surface.get_width() / 2
    turn_text_y = 15
    screen.blit(small_surface, (turn_text_x, turn_text_y))

    pygame.display.update((turn_text_x, turn_text_y, small_surface.get_width(), small_surface.get_height()))


def start_program():
    pygame.init()
    pygame.display.set_caption("Checkers")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Game state
    game_state = "start"

    game = None
    first_turn = DARK

    title_font = pygame.font.SysFont("arialblack", 40)
    text_font = pygame.font.SysFont("arialblack", 20)
    small_font = pygame.font.SysFont("arialblack", 15)
    text_colour = WHITE

    # Buttons
    return_img = pygame.image.load('assets/return.png').convert_alpha()
    return_button = Button(return_img, (SCREEN_WIDTH - 150, 10))
    easy_img = pygame.image.load('assets/easy.png').convert_alpha()
    easy_button = Button(easy_img, (0, 200))
    medium_img = pygame.image.load('assets/medium.png').convert_alpha()
    medium_button = Button(medium_img, (0, 300))
    hard_img = pygame.image.load('assets/hard.png').convert_alpha()
    hard_button = Button(hard_img, (0, 400))

    img_pvp = pygame.image.load('assets/pvp.png').convert_alpha()
    button_pvp = Button(img_pvp, (0, 150))
    img_pva = pygame.image.load('assets/pva.png').convert_alpha()
    button_pva = Button(img_pva, (0, 250))
    img_ava = pygame.image.load('assets/ava.png').convert_alpha()
    button_ava = Button(img_ava, (0, 350))
    img_exit = pygame.image.load('assets/exit.png').convert_alpha()
    button_exit = Button(img_exit, (0, 450))

    # Turn surface
    dark_turn_surface = pygame.Surface((150, 30))
    dark_turn_surface.fill((50, 75, 105))
    draw_text(dark_turn_surface, "Dark Turn", text_font, text_colour, (0, 0))
    light_turn_surface = pygame.Surface((150, 30))
    light_turn_surface.fill((50, 75, 105))
    draw_text(light_turn_surface, "Light Turn", text_font, text_colour, (0, 0))

    # game loop
    running = True
    while running:

        # Closes the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Run start screen
        if game_state == "start":
            screen.fill((50, 75, 105))

            draw_text_center(screen, "Checkers", title_font, text_colour, 50)
            button_pvp.draw_self_center(screen)
            button_pva.draw_self_center(screen)
            button_ava.draw_self_center(screen)
            button_exit.draw_self_center(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if button_pvp.rect.collidepoint(x, y):
                            print("pVp")
                            game_state = "pvp"
                            game = Game(screen, first_turn)
                        if button_pva.rect.collidepoint(x, y):
                            print("Pva")
                            game_state = "select ai"
                            game = Game(screen, first_turn)
                        if button_ava.rect.collidepoint(x, y):
                            print("aVA")
                            game_state = "select dark ai"
                            game = Game(screen, first_turn)
                        if button_exit.rect.collidepoint(x, y):
                            print("exiting")
                            running = False

            pygame.display.update()

        if game_state == "pvp":
            screen.fill((50, 75, 105))
            draw_text(screen, "Vs Player", text_font, text_colour, (50, 15))
            return_button.draw_self(screen)
            pygame.draw.rect(screen, BOARD_DARK, game.board_area)
            game.draw_board()
            game.check_for_moves()
            game.draw_selected_sq()
            game.draw_possible_moves()

            if game.current_turn is DARK:
                screen.blit(dark_turn_surface, (245, 15))
            else:
                screen.blit(light_turn_surface, (245, 15))

            if game.check_game_over():
                winner_text = "Dark player wins!" if game.winner is DARK else "Light player wins!"
                draw_text(screen, "Game Over! " + winner_text, text_font, text_colour, (150, 560))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if game.board_area.collidepoint(x, y):  # if mouse click within the board area
                            game.select_square(x, y)
                        elif return_button.rect.collidepoint(x, y):
                            game_state = "start"

        if game_state == "select ai":
            screen.fill((50, 75, 105))
            draw_text_center(screen, "AI Settings", title_font, text_colour, 100)
            return_button.draw_self(screen)
            easy_button.draw_self_center(screen)
            medium_button.draw_self_center(screen)
            hard_button.draw_self_center(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if return_button.rect.collidepoint(x, y):
                            game_state = "start"
                        if easy_button.rect.collidepoint(x, y):
                            game_state = "pva"
                            ai_level = 3
                        if medium_button.rect.collidepoint(x, y):
                            game_state = "pva"
                            ai_level = 5
                        if hard_button.rect.collidepoint(x, y):
                            game_state = "pva"
                            ai_level = 7

        if game_state == "pva":
            screen.fill((50, 75, 105))
            draw_text(screen, "Vs AI", text_font, text_colour, (50, 15))
            return_button.draw_self(screen)
            pygame.draw.rect(screen, BOARD_DARK, game.board_area)
            game.draw_board()
            game.check_for_moves()
            game.draw_selected_sq()
            game.draw_possible_moves()
            if game.current_turn is DARK:
                screen.blit(dark_turn_surface, (245, 15))
            else:
                screen.blit(light_turn_surface, (245, 15))

            if game.check_game_over():
                winner_text = "Dark player wins!" if game.winner is DARK else "Light player wins!"
                draw_text(screen, "Game Over! " + winner_text, text_font, text_colour, (150, 560))

            pygame.display.update()

            if game.current_turn is LIGHT and not game.check_game_over():
                start_time = time.time()
                if ai_level == 7:
                    eval_score, best_move = ai_algorithm.minimax_hard(game.board, 7, True, LIGHT)
                elif ai_level == 5:
                    eval_score, best_move = ai_algorithm.minimax_medium(game.board, 5, True, LIGHT)
                else:
                    eval_score, best_move = ai_algorithm.minimax_easy(game.board, 3, True, LIGHT)
                print(time.time() - start_time)
                print("eval_score, best_move")
                print(eval_score, best_move)

                if best_move is not None:
                    time.sleep(0.15)
                    game.board.move_piece(best_move)
                    ai_algorithm.reset_history_table()
                    game.change_turn()

                print("eval_score, best_move")
                print(game.board.light_kings)
                print(game.board.dark_kings)
                print(game.board.light_pieces)
                print(game.board.dark_pieces)

                print("Eval count:")
                print(ai_algorithm.get_eval_count())
                ai_algorithm.reset_eval_count()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if game.board_area.collidepoint(x, y):
                            game.select_square(x, y)
                        elif return_button.rect.collidepoint(x, y):
                            game_state = "start"

        if game_state == "select dark ai":
            screen.fill((50, 75, 105))
            draw_text_center(screen, "Dark AI Settings", title_font, text_colour, 100)
            return_button.draw_self(screen)
            easy_button.draw_self_center(screen)
            medium_button.draw_self_center(screen)
            hard_button.draw_self_center(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if return_button.rect.collidepoint(x, y):
                            game_state = "start"
                        if easy_button.rect.collidepoint(x, y):
                            game_state = "select light ai"
                            dark_ai_level = 3
                        if medium_button.rect.collidepoint(x, y):
                            game_state = "select light ai"
                            dark_ai_level = 5
                        if hard_button.rect.collidepoint(x, y):
                            game_state = "select light ai"
                            dark_ai_level = 7

        if game_state == "select light ai":
            screen.fill((50, 75, 105))
            draw_text_center(screen, "Light AI Settings", title_font, text_colour, 100)
            return_button.draw_self(screen)
            easy_button.draw_self_center(screen)
            medium_button.draw_self_center(screen)
            hard_button.draw_self_center(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if return_button.rect.collidepoint(x, y):
                            game_state = "select dark ai"
                        if easy_button.rect.collidepoint(x, y):
                            game_state = "ava"
                            light_ai_level = 3
                        if medium_button.rect.collidepoint(x, y):
                            game_state = "ava"
                            light_ai_level = 5
                        if hard_button.rect.collidepoint(x, y):
                            game_state = "ava"
                            light_ai_level = 7

        if game_state == "ava":
            fast = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                fast = True  # Toggle the fast flag when space is pressed

            screen.fill((50, 75, 105))
            draw_text(screen, "AI Vs AI", text_font, text_colour, (40, 15))
            return_button.draw_self(screen)
            draw_text(screen, "Hold SPACE", small_font, text_colour, (485, 555))
            draw_text(screen, "to speed up", small_font, text_colour, (487, 570))

            if game.current_turn is DARK:
                screen.blit(dark_turn_surface, (245, 15))
            else:
                screen.blit(light_turn_surface, (245, 15))
            pygame.draw.rect(screen, BOARD_DARK, game.board_area)
            game.draw_board()
            game.check_for_moves()
            if game.check_game_over():
                winner_text = "Dark player wins!" if game.winner is DARK else "Light player wins!"
                draw_text(screen, "Game Over! " + winner_text, text_font, text_colour, (150, 560))

            pygame.display.update()

            if game.current_turn is LIGHT and not game.check_game_over():
                start_time = time.time()
                if light_ai_level == 7:
                    eval_score, best_move = ai_algorithm.minimax_hard(game.board, 7, True, LIGHT)
                elif light_ai_level == 5:
                    eval_score, best_move = ai_algorithm.minimax_medium(game.board, 5, True, LIGHT)
                else:
                    eval_score, best_move = ai_algorithm.minimax_easy(game.board, 3, True, LIGHT)
                print(time.time() - start_time)
                print("eval_score, best_move")
                print(eval_score, best_move)

                if best_move is not None:
                    if light_ai_level != 7:
                        if not fast:
                            time.sleep(1)
                    game.board.move_piece(best_move)
                    ai_algorithm.reset_history_table()
                    game.change_turn()
                    print("DARJ")
                    print(game.current_turn)

                print("eval_score, best_move")
                print(game.board.light_kings)
                print(game.board.dark_kings)
                print(game.board.light_pieces)
                print(game.board.dark_pieces)

                print("Eval count:")
                print(ai_algorithm.get_eval_count())
                ai_algorithm.reset_eval_count()

            if not fast:
                game.draw_board()
                game.check_for_moves()
                pygame.display.update()

            if game.current_turn is DARK:
                screen.blit(dark_turn_surface, (245, 15))
            else:
                screen.blit(light_turn_surface, (245, 15))
            pygame.display.update((245, 15, 150, 30))

            if game.current_turn is DARK and not game.check_game_over():
                start_time = time.time()
                if dark_ai_level == 7:
                    eval_score, best_move = ai_algorithm.minimax_hard(game.board, 7, True, DARK)
                elif dark_ai_level == 5:
                    eval_score, best_move = ai_algorithm.minimax_medium(game.board, 5, True, DARK)
                else:
                    eval_score, best_move = ai_algorithm.minimax_easy(game.board, 3, True, DARK)
                print(time.time() - start_time)
                print("eval_score, best_move")
                print(eval_score, best_move)

                if best_move is not None:
                    if dark_ai_level != 7:
                        if not fast:
                            time.sleep(1)
                    game.board.move_piece(best_move)
                    ai_algorithm.reset_history_table()
                    game.change_turn()
                    print("LGIHT")
                    print(game.current_turn)

                print("eval_score, best_move")
                print(game.board.light_kings)
                print(game.board.dark_kings)
                print(game.board.light_pieces)
                print(game.board.dark_pieces)

                print("Eval count:")
                print(ai_algorithm.get_eval_count())
                ai_algorithm.reset_eval_count()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        if return_button.rect.collidepoint(x, y):
                            game_state = "start"

        pygame.display.update()
    pygame.quit()


start_program()
