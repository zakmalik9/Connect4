import math
import random
from WinManager import WinManager


class MiniMax(WinManager):

    def evaluate_window(self, window, maximising_piece, minimising_piece):
        score = 0
        if window.count(maximising_piece) == 4:
            score += 100
        elif window.count(maximising_piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(maximising_piece) == 2 and window.count(0) == 2:
            score += 2
        if window.count(minimising_piece) == 4:
            score -= 99
        elif window.count(minimising_piece) == 3 and window.count(0) == 1:
            score -= 4
        elif window.count(minimising_piece) == 2 and window.count(0) == 2:
            score -= 1
        return score


    def score_position(self, board, maximising_piece, minimising_piece, row_count, column_count):
        score = 0
        # Score Center
        center_array = [int(i) for i in list(board[:, column_count // 2])]
        center_count = center_array.count(maximising_piece)
        score += center_count * 3
        # score +=
        # Score Horizontal
        for r in range(row_count):
            r_array = [int(i) for i in list(board[r, :])]
            for col in range(column_count - 3):
                window = r_array[col:col + 4]
                score += self.evaluate_window(window, maximising_piece, minimising_piece)
        # Score Vertical
        for col in range(column_count):
            col_array = [int(i) for i in list(board[:, col])]
            for r in range(row_count - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, maximising_piece, minimising_piece)
        # Score +Diagonals
        for r in range(row_count - 3):
            for col in range(column_count - 3):
                window = [board[r + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, maximising_piece, minimising_piece)
        # Score -Diagonals
        for r in range(row_count - 3):
            for col in range(column_count - 3):
                window = [board[r + 3 - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, maximising_piece, minimising_piece)
        return score


    def get_valid_locations(self, board, column_count, row_count, default_piece):
        valid_locations = []
        for c in range(column_count):
            if self.is_valid_location(row_count, default_piece, board, c):
                valid_locations.append(c)
        return valid_locations


    def is_terminal_node(self, board, maximising_piece, minimising_piece, column_count, row_count, default_piece):
        return self.check_for_win(board, maximising_piece) or self.check_for_win(board, minimising_piece) or \
               len(self.get_valid_locations(board, column_count, row_count, default_piece)) == 0


    def execute_minimax(self, node, depth, alpha, beta, maximising_player, maximising_piece, minimising_piece,
                        row_count, column_count, default_piece):
        valid_locations = self.get_valid_locations(node, column_count, row_count, default_piece)
        best_col = random.choice(valid_locations)
        if depth == 0 or self.is_terminal_node(node, maximising_piece, minimising_piece, column_count, row_count,
                                               default_piece):
            if self.is_terminal_node(node, maximising_piece, minimising_piece, column_count, row_count, default_piece):
                if self.check_for_win(node, maximising_piece):
                    return None, 1000000
                elif self.check_for_win(node, minimising_piece):
                    return None, -1000000
                else:
                    return None, 0
            else:
                return None, self.score_position(node, maximising_piece, minimising_piece, row_count, column_count)
        if maximising_player:
            value = -math.inf
            for col in valid_locations:
                r = self.get_next_open_row(row_count, default_piece, node, col)
                brd_copy = node.copy()
                self.drop_piece(brd_copy, r, col, maximising_piece)
                new_score = self.execute_minimax(brd_copy, depth - 1, alpha, beta, False, maximising_piece,
                                                 minimising_piece, row_count, column_count, default_piece)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:
            value = math.inf
            for col in valid_locations:
                r = self.get_next_open_row(row_count, default_piece, node, col)
                brd_copy = node.copy()
                self.drop_piece(brd_copy, r, col, minimising_piece)
                new_score = self.execute_minimax(brd_copy, depth - 1, alpha, beta, True, maximising_piece,
                                                 minimising_piece, row_count, column_count, default_piece)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return best_col, value
