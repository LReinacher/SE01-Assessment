import numpy as np
import sys


class SlidingGame:
    def __init__(self):
        self._board = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, np.NaN, 12], [13, 14, 11, 15]])
        self._valid_numbers = self._board[~np.isnan(self._board)]

    def is_number_valid(self, number: int):
        return number in self._valid_numbers
        
    def _print_board(self):
        print(self._board)

    def _get_piece_position(self, value):
        pos = np.where(np.isnan(self._board)) if np.isnan(value) else np.where(self._board == value)
        if pos[0].size == 0:
            return None
        return pos

    @staticmethod
    def _is_move_allowed(piece_pos: np.array, empty_pos: np.array):
        if piece_pos[0] == empty_pos[0] and (1 >= piece_pos[1] - empty_pos[1] >= -1):
            return True
        elif piece_pos[1] == empty_pos[1] and (1 >= piece_pos[0] - empty_pos[0] >= -1):
            return True
        return False

    def _move_piece(self, piece_pos: np.array, empty_pos: np.array):
        self._board[empty_pos] = self._board[piece_pos]
        self._board[piece_pos] = None

    def _is_board_ordered(self):
        try:
            np.testing.assert_equal(np.sort(self._board[~np.isnan(self._board)]), self._board[~np.isnan(self._board)])
        except AssertionError:
            return False
        return True

    def _move_piece_by_number(self, number: int):
        piece_pos, empty_pos = self._get_piece_position(number), self._get_piece_position(np.NaN)
        if self._is_move_allowed(piece_pos, empty_pos):
            self._move_piece(piece_pos, empty_pos)
            return True
        return False

    def play(self):
        print("--- SLIDING PUZZLE ---")
        self._print_board()
        print("Please enter the number of the piece you want to move")
        while not self._is_board_ordered():
            piece = input(">> ")
            try:
                piece_number = int(piece)
                if not game.is_number_valid(piece_number):
                    raise TypeError
                if not self._move_piece_by_number(piece_number):
                    print("This move is not allowed!")
                    continue
                self._print_board()
            except TypeError:
                print("Invalid number, please try again")

        print("GAME WON!")
        sys.exit(0)

if __name__ == "__main__":
    game = SlidingGame()
    game.play()