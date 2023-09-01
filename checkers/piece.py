from constants import DARK, LIGHT, DIM_GREY, SQ_SIZE


class Piece:
    def __init__(self, colour):
        self.colour = colour
        self.is_king = False
        self.value = 1

    def __repr__(self):
        if self.colour == DARK:
            return "D"
        if self.colour == LIGHT:
            return "L"

    def get_colour(self):
        if self:
            return self.colour
        else:
            return None

    def get_is_king(self):
        if self:
            return self.is_king
        else:
            return None

    def get_value(self):
        if self:
            return self.value
        else:
            return 0

    def set_is_king(self, boolean):
        self.is_king = boolean

    def set_value(self, value):
        self.value = value


