from constants import BLACK, WHITE, DARK, LIGHT, BOARD_DARK, BOARD_LIGHT


class Square:
    def __init__(self, colour, row, column, piece):
        self.colour = colour
        self.row = row
        self.column = column
        self.piece = piece

    def __repr__(self):
        if self.colour == BOARD_DARK:
            if self.piece:
                if self.piece.colour == DARK:
                    return "B_SQ-D_P"
                else:
                    return "B_SQ-L_P"
            return "B_SQ-None"
        if self.colour == BOARD_LIGHT:
            return "W_SQ"

    def get_colour(self):
        if self is None:
            return None
        else:
            return self.colour

    def get_piece(self):
        return self.piece

    def get_piece_colour(self):
        if self.piece is None:
            return None
        else:
            return self.piece.colour

    def get_row(self):
        return self.row

    def get_col(self):
        return self.column

    def get_sq_pos(self):
        return self.row, self.column

    def set_colour(self, colour):
        self.colour = colour

    def set_piece(self, piece):
        self.piece = piece

    def find_neighbours(self):
        neighbours = []
        if self.row > 0 and self.column > 0:
            neighbours.append((self.row - 1, self.column - 1))
        if self.row > 0 and self.column < 7:
            neighbours.append((self.row - 1, self.column + 1))
        if self.row < 7 and self.column > 0:
            neighbours.append((self.row + 1, self.column - 1))
        if self.row < 7 and self.column < 7:
            neighbours.append((self.row + 1, self.column + 1))
        return neighbours
