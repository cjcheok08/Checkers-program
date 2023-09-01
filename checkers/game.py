import pygame

from checkers.board import Board
from constants import BLACK, SQ_SIZE, DARK, BOARD_OFFSET, BOARD_SIZE, LIME_GREEN, RED, LIGHT, \
    BOARD_DARK


class Game:  # handles the rendering and the game flow
    def __init__(self, screen, first_turn):
        self.screen = screen
        self.board = Board()
        self.board_area = pygame.Rect(BOARD_OFFSET, BOARD_OFFSET, BOARD_SIZE, BOARD_SIZE)  # render area for board
        self.current_turn = first_turn
        self.board.turn = first_turn
        self.board.find_all_possible_moves(self.current_turn)
        self.selected_square = None
        self.winner = None

    def change_turn(self):
        if self.current_turn == DARK:
            self.current_turn = LIGHT
        elif self.current_turn == LIGHT:
            self.current_turn = DARK
        self.board.find_all_possible_moves(self.current_turn)
        self.check_game_over()
        self.selected_square = None

    def check_game_over(self):
        if self.board.no_moves_left():
            self.winner = DARK if self.current_turn is LIGHT else LIGHT
            return True
        else:
            return False

    def draw_board(self):
        # draw_square
        for row, board_rep_row in enumerate(self.board.get_board_rep()):
            for col, square in enumerate(board_rep_row):

                square_x = self.board_area.left + (col * SQ_SIZE)
                square_y = self.board_area.top + (row * SQ_SIZE)

                square_rect = pygame.Rect(square_x, square_y, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(self.screen, square.get_colour(), square_rect)

                piece = square.get_piece()
                if piece:
                    piece_x = square_x + (SQ_SIZE // 2)
                    piece_y = square_y + (SQ_SIZE // 2)
                    radius = SQ_SIZE // 3
                    pygame.draw.circle(self.screen, piece.get_colour(), (piece_x, piece_y), radius)
                    pygame.draw.circle(self.screen, BLACK, (piece_x, piece_y), radius + 2, 2)
                    if piece.get_is_king():
                        crown_img = pygame.image.load('assets/king.png').convert_alpha()
                        width, height = crown_img.get_size()
                        scaled_image = pygame.transform.scale(crown_img, (width // 1.17, height // 1.17))
                        self.screen.blit(scaled_image, (
                            piece_x - scaled_image.get_width() // 2, piece_y - scaled_image.get_height() // 2))
                    else:
                        pygame.draw.circle(self.screen, BLACK, (piece_x, piece_y), radius - 5, 2)

    def check_for_moves(self):  # draw possible moves for selected square if exists
        all_start_squares = self.board.all_possible_moves.keys()
        for start_sq in all_start_squares:
            start_row, start_col = start_sq
            end_x = self.board_area.left + (start_col * SQ_SIZE)
            end_y = self.board_area.top + (start_row * SQ_SIZE)
            pygame.draw.rect(self.screen, 'blue', pygame.Rect(end_x, end_y, SQ_SIZE, SQ_SIZE), 4, 0)

    def draw_selected_sq(self):
        if self.selected_square:
            selected_x = self.board_area.left + (self.selected_square.column * SQ_SIZE)
            selected_y = self.board_area.top + (self.selected_square.row * SQ_SIZE)
            pygame.draw.rect(self.screen, LIME_GREEN, pygame.Rect(selected_x, selected_y, SQ_SIZE, SQ_SIZE), 4, 0)

    def draw_possible_moves(self):
        if self.selected_square:
            selected_sq_pos = (self.selected_square.get_row(), self.selected_square.get_col())
            if selected_sq_pos in self.board.all_possible_moves.keys():
                end_squares = self.board.all_possible_moves[selected_sq_pos]
                for end_sq in end_squares:  # loop through all keys in end_squares dict
                    end_row, end_col = end_sq
                    end_x = self.board_area.left + (end_col * SQ_SIZE)
                    end_y = self.board_area.top + (end_row * SQ_SIZE)
                    pygame.draw.rect(self.screen, 'green', pygame.Rect(end_x, end_y, SQ_SIZE, SQ_SIZE), 4, 0)
                    if end_squares[end_sq] is not None:
                        for captured_piece in end_squares[end_sq]:
                            captured_row, captured_col = captured_piece
                            captured_x = self.board_area.left + (captured_col * SQ_SIZE)
                            captured_y = self.board_area.top + (captured_row * SQ_SIZE)
                            pygame.draw.rect(self.screen, RED, pygame.Rect(captured_x, captured_y, SQ_SIZE, SQ_SIZE), 4,
                                             0)

    def select_square(self, x, y):
        row = int((y - self.board_area.top) // SQ_SIZE)
        col = int((x - self.board_area.left) // SQ_SIZE)

        if self.selected_square:  # if a square is already selected
            move_result = self.board.player_move(self.selected_square, (row, col))
            if move_result is False:  # if not moved
                self.set_selected_square((row, col))
            elif move_result is True:  # if successfully moved, change turn
                self.change_turn()
        else:
            self.set_selected_square((row, col))

    def set_selected_square(self, sq_pos):
        row, col = sq_pos
        square = self.board.get_square((row, col))
        if square.get_colour() is BOARD_DARK and square.get_piece_colour() is self.current_turn:
            self.selected_square = square
