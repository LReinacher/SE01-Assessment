import numpy as np
import sys
import random


class SlidingGameMatch:
    def __init__(self, board_size, board_generation_moves):
        self._board_size = board_size
        self._board_generation_moves = board_generation_moves
        self._board = self._create_board_of_n_size(self._board_size)
        self._generate_board()
        self._valid_numbers = self._board[~np.isnan(self._board)]
        self._move_counter = 0

    @staticmethod
    def _create_board_of_n_size(size: int):
        return np.array(list(range(1, size * size)) + [np.nan]).reshape([size, size])

    def is_number_valid(self, number: int):
        return number in self._valid_numbers
        
    def _print_board(self):
        print(self._board)

    def _get_piece_position(self, value):
        pos = np.where(np.isnan(self._board)) if np.isnan(value) else np.where(self._board == value)
        if pos[0].size == 0:
            return None
        return pos

    def _is_move_allowed(self, piece_pos: np.array, empty_pos: np.array):
        if not piece_pos[0][0] > 0 or not piece_pos[0][0] < self._board.shape[1]:
            return False
        if not piece_pos[1][0] > 0 or not piece_pos[1][0] < self._board.shape[0]:
            return False
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

    def _get_random_move(self, last_pos=None):
        curr_pos = self._get_piece_position(np.NaN)
        possible_new_pos = [
            tuple([curr_pos[0], np.array([curr_pos[1][0] + 1])]),
            tuple([curr_pos[0], np.array([curr_pos[1][0] - 1])]),
            tuple([np.array([curr_pos[0][0] + 1]), curr_pos[1]]),
            tuple([np.array([curr_pos[0][0] - 1]), curr_pos[1]])
        ]
        valid_new_pos = []
        for new_pos in possible_new_pos:
            if self._is_move_allowed(new_pos, curr_pos) and last_pos != new_pos:
                valid_new_pos.append(new_pos)
        return random.choice(valid_new_pos), curr_pos


    def _generate_board(self):
        last_pos = None
        for move_index in range(0, self._board_generation_moves):
            new_pos, cur_pos = self._get_random_move(last_pos)
            self._move_piece(new_pos, cur_pos)
            last_pos = cur_pos


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
    BOARD_SIZE = 4
    BOARD_GENERATION_MOVES = 60

    def __init__(self):
        self._matches_moves_counter = np.array([np.NaN, np.NaN, np.NaN])
        
    def play(self):
        print("--- SLIDING PUZZLE ---")
        for match_number in range(0, self._matches_moves_counter.size):
            print("++++ MATCH {} ++++".format(match_number + 1))
            print("Please enter the number of the piece you want to move")
            match = SlidingGameMatch(self.BOARD_SIZE, self.BOARD_GENERATION_MOVES)
            self._matches_moves_counter[match_number] = match.play_match()
            print("==== MATCH FINISHED ====".format(match_number + 1))
        print("In your best match, you needed {} moves to solve the puzzle!".format(int(self._matches_moves_counter.min())))

            

if __name__ == "__main__":
    game = SlidingGame()
    game.play()