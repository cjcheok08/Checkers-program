from collections import deque

from checkers.piece import Piece
from checkers.square import Square
from constants import LIGHT, DARK, BOARD_DARK, BOARD_LIGHT
from constants import ROWS, COLUMNS


class Board:  # Will not be passed screen, all rendering will be handled by Game
    def __init__(self):
        self.board_rep = []
        self.starting_board()
        # self.test_board2()
        self.dark_pieces = 12
        self.light_pieces = 12
        self.dark_kings = 0
        self.light_kings = 0
        self.all_possible_moves = dict()
        self.capture_possible = False
        self.turn = None

    # SETTING UP THE BOARD
    # Create a 2D array which represents the checkers board representation; set pieces to starting position
    # Populate the empty board with the starting position pieces
    def starting_board(self):
        for row in range(ROWS):
            row_list = []
            for col in range(COLUMNS):
                if (row + col) % 2 != 0:  # Dark squares according to checker pattern
                    # Set up initial piece positions
                    if row <= 2:  # Row 0-2
                        piece = Piece(LIGHT)
                    elif 2 < row < 5:  # Row 3-4
                        piece = None
                    else:  # Row 5-7
                        piece = Piece(DARK)

                    row_list.append(Square(BOARD_DARK, row, col, piece))  # Dark square
                else:
                    row_list.append(Square(BOARD_LIGHT, row, col, None))  # Light square
            self.board_rep.append(row_list)  # Appends an 8-item list into the empty list 8 times
        print(self.board_rep)  # For ease of view

    def test_board(self):
        for row in range(ROWS):
            row_list = []
            for col in range(COLUMNS):
                if (row + col) % 2 != 0:  # dark square according to checker sequence
                    row_list.append(Square(BOARD_DARK, row, col, None))  # dark square
                else:
                    row_list.append(Square(BOARD_LIGHT, row, col, None))  # light square
            self.board_rep.append(row_list)  # appends an 8-item list into the empty list 8 times
        # self.board_rep[5][2].set_piece(Piece(DARK))
        # self.board_rep[6][5].set_piece(Piece(LIGHT))
        # self.board_rep[7][6].set_piece(Piece(DARK))
        self.board_rep[2][1].set_piece(Piece(DARK))

        self.board_rep[3][2].set_piece(Piece(LIGHT))
        self.board_rep[1][2].set_piece(Piece(LIGHT))
        self.board_rep[1][4].set_piece(Piece(LIGHT))
        self.board_rep[6][1].set_piece(Piece(LIGHT))
        self.board_rep[6][3].set_piece(Piece(LIGHT))
        self.board_rep[6][5].set_piece(Piece(LIGHT))
        self.board_rep[2][3].set_piece(Piece(LIGHT))

    def test_board2(self):
        for row in range(ROWS):
            row_list = []
            for col in range(COLUMNS):
                if (row + col) % 2 != 0:  # dark square according to checker sequence
                    row_list.append(Square(BOARD_DARK, row, col, None))  # dark square
                else:
                    row_list.append(Square(BOARD_LIGHT, row, col, None))  # light square
            self.board_rep.append(row_list)  # appends an 8-item list into the empty list 8 times
        self.board_rep[5][2].set_piece(Piece(DARK))
        # self.board_rep[7][6].set_piece(Piece(DARK))

        # self.board_rep[6][5].set_piece(Piece(LIGHT))
        self.board_rep[4][3].set_piece(Piece(LIGHT))
        self.board_rep[4][1].set_piece(Piece(LIGHT))
        # self.board_rep[2][1].set_piece(Piece(LIGHT))
        self.board_rep[2][3].set_piece(Piece(LIGHT))
        self.board_rep[2][5].set_piece(Piece(LIGHT))

    # Searching for all legal moves
    # For all your pieces, check going through all possible moves, and add to dict by {start: [end sq, [captured]}"
    def find_all_possible_moves(self, current_turn):
        self.turn = current_turn
        self.reset_all_possible_moves()
        capture_moves = dict()
        ordinary_moves = dict()

        for row, board_rep_row in enumerate(self.get_board_rep()):
            for col, square in enumerate(board_rep_row):
                # if WHITE squares, skip checking
                if (row + col) % 2 == 0:
                    continue

                # if BLACK squares, check for current turn pieces
                if square.get_piece() and square.get_piece_colour() is current_turn:  # for each current turn piece
                    end_squares = dict()  # dict with end_sq as keys and captured pieces as values if there are
                    is_king = square.get_piece().get_is_king()

                    self.find_capture_moves((row, col), is_king, end_squares, current_turn)  # pass in the list
                    if end_squares:  # if dict is not empty, if captures are possible
                        self.capture_possible = True
                        capture_moves[(row, col)] = end_squares
                        ordinary_moves.clear()

                    if not self.capture_possible:
                        self.find_ordinary_moves((row, col), is_king, end_squares, current_turn)
                        if end_squares:
                            ordinary_moves[(row, col)] = end_squares

        if capture_moves:
            self.all_possible_moves.update(capture_moves)  # add this dict to all_possible_moves
        if ordinary_moves:
            self.all_possible_moves.update(ordinary_moves)  # add this dict to all_possible_moves

    def find_capture_moves(self, sq_pos, is_king, end_squares, turn):
        directions = [(-1, 1), (-1, -1)] if turn is DARK else [(1, -1), (1, 1)]
        if is_king:
            directions = [(-1, 1), (-1, -1), (1, -1), (1, 1)]

        visited = set()
        captured = []
        stack = deque([(sq_pos, visited, captured)])

        while stack:
            (row, col), visited, captured = stack.pop()
            can_jump = False

            if not self.within_bounds(row, col):
                continue

            visited.add((row, col))

            # Look in all directions
            for d_row, d_col in directions:
                if self.within_bounds(row + d_row, col + d_col) and self.within_bounds(row + 2 * d_row,
                                                                                       col + 2 * d_col):

                    if (row + d_row, col + d_col) not in captured:
                        if self.get_square((row + d_row, col + d_col)).get_piece() and \
                                self.get_square((row + d_row, col + d_col)).get_piece_colour() != turn and \
                                self.get_square((row + 2 * d_row, col + 2 * d_col)).get_piece() is None:
                            captured_copy = captured.copy()
                            captured_copy.append((row + d_row, col + d_col))
                            stack.append(((row + 2 * d_row, col + 2 * d_col), visited.copy(), captured_copy))
                            can_jump = True

            # If captured a piece in this iteration AND can no longer jump again
            if captured and not can_jump:
                end_squares[(row, col)] = captured

    def find_ordinary_moves(self, sq_pos, is_king, end_squares, current_turn):
        directions = [(-1, 1), (-1, -1)] if current_turn is DARK else [(1, -1), (1, 1)]
        if is_king:
            directions = [(-1, 1), (-1, -1), (1, -1), (1, 1)]

        row, col = sq_pos
        for d_row, d_col in directions:  # check all diagonal directions (right, left)
            if self.within_bounds(row + d_row, col + d_col):
                if self.board_rep[row + d_row][col + d_col].get_piece() is None:
                    end_squares[(row + d_row, col + d_col)] = None

    def within_bounds(self, row, col):
        return 0 <= row < ROWS and 0 <= col < COLUMNS

    def reset_all_possible_moves(self):
        self.all_possible_moves.clear()
        self.capture_possible = False  # reset for next turn

    def player_move(self, start_sq, end_sq_pos):  # make_move()/ player_move_check
        all_possible_moves = self.all_possible_moves
        start_sq_pos = start_sq.get_sq_pos()

        if start_sq_pos in all_possible_moves.keys() and end_sq_pos in all_possible_moves[start_sq_pos].keys():
            self.move_piece((start_sq_pos, end_sq_pos))
            return True
        else:
            return False

    def move_piece(self, move):
        start_sq_pos, end_sq_pos = move

        start_sq = self.get_square(start_sq_pos)
        end_sq = self.get_square(end_sq_pos)
        end_sq.set_piece(start_sq.get_piece())
        start_sq.set_piece(None)

        if self.capture_possible:
            captured_pieces = self.all_possible_moves[start_sq_pos][end_sq_pos]
            for piece_pos in captured_pieces:
                square = self.get_square(piece_pos)
                if square.get_piece_colour() is LIGHT:
                    if square.get_piece().get_is_king():
                        self.light_kings -= 1
                    else:
                        self.light_pieces -= 1
                elif square.get_piece_colour() is DARK:
                    if square.get_piece().get_is_king():
                        self.dark_kings -= 1
                    else:
                        self.dark_pieces -= 1
                square.set_piece(None)

        if end_sq_pos[0] == 0 or end_sq_pos[0] == 7:
            piece = self.get_square(end_sq_pos).get_piece()
            self.promote_piece(piece)

    def promote_piece(self, piece):
        if not piece.get_is_king():
            piece.set_is_king(True)
            piece.set_value(3)
            if piece.get_colour() is LIGHT:
                self.light_kings += 1
                self.light_pieces -= 1
            else:
                self.dark_kings += 1
                self.dark_pieces -= 1

    def no_moves_left(self):
        if not self.all_possible_moves:  # if the current player has no possible moves
            return True
        else:
            return False

    def get_board_rep(self):
        return self.board_rep

    def get_square(self, sq_pos):
        sq_row, sq_col = sq_pos
        return self.board_rep[sq_row][sq_col]
