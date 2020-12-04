import numpy as np
import sys


class SlidingGameMatch:
    def __init__(self):
        self._board = np.array([[1, 2, 3], [5, 6, 7], [9, 10, np.NaN], [13, 14, 11]])
        self._valid_numbers = self._board[~np.isnan(self._board)]
        self._move_counter = 0

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

    def play_match(self):
        self._print_board()
        while not self._is_board_ordered():
            piece = input(">> ")
            try:
                piece_number = int(piece)
                if not self.is_number_valid(piece_number):
                    raise TypeError
                if not self._move_piece_by_number(piece_number):
                    print("This move is not allowed!")
                    continue
                self._move_counter += 1
                self._print_board()
            except TypeError:
                print("Invalid number, please try again")

        return self._move_counter
        
class SlidingGame:
    def __init__(self):
        self._matches_moves_counter = np.array([np.NaN, np.NaN, np.NaN])
        
    def play(self):
        print("--- SLIDING PUZZLE ---")
        for match_number in range(0, self._matches_moves_counter.size):
            print("++++ MATCH {} ++++".format(match_number + 1))
            print("Please enter the number of the piece you want to move")
            match = SlidingGameMatch()
            self._matches_moves_counter[match_number] = match.play_match()
            print("==== MATCH FINISHED ====".format(match_number + 1))
        print("In your best match, you needed {} moves to solve the puzzle!".format(int(self._matches_moves_counter.min())))

            

if __name__ == "__main__":
    game = SlidingGame()
    game.play()