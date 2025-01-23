import random


class Puzzle8:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.numbers = [f'{i}' for i in range(1, 9)]  # Form 1 to 8
        self.numbers.append(' ')  # Add a blank slot for moving

    def fill_board(self):
        list_of_nums = list(self.numbers)
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                item = random.choice(list_of_nums)  # Take a random value
                self.board[row][column] = item  # Add the chosen value to the board
                list_of_nums.remove(item)  # Remove the chosen value from the list to avoid choosing it again

    def display_board(self):
        for row in self.board:
            print(' | '.join(row))
            print('-' * 9)

    def is_solved(self) -> bool:
        return self.board == [
            ['1', '2', '3'],
            ['8', ' ', '4'],
            ['7', '6', '5']
        ]

    def move(self, direction: str) -> bool:
        """Move the blank slot in the given direction
        @param direction: str: 'up', 'down', 'left', or 'right'
        @return: True if the move was successful, False otherwise
        """
        #  Using comprehension for loop to get the position of the blank slot
        # blank_position = \
        #     [(row_i, col_i) for row_i, row in enumerate(self.board) for col_i, col in enumerate(row) if col == ' '][0]

        # Using normal for loop to get the position of the blank slot
        blank_position = None
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if col == ' ':
                    blank_position = (row_index, col_index)
                    break
            if blank_position:
                break

        row, col = blank_position

        # Define the possible moves
        moves = {
            'up': (row - 1, col),
            'down': (row + 1, col),
            'left': (row, col - 1),
            'right': (row, col + 1)
        }

        if direction in moves:
            new_row, new_col = moves[direction]
            # Check if the new position is within the board limits
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Swap the blank slot with the new position
                self.board[row][col], self.board[new_row][new_col] = self.board[new_row][new_col], self.board[row][col]
                return True
        return False

    def alpha_beta(self, is_maximizing: bool, depth: int, alpha=float('-inf'), beta=float('inf')):
        if self.is_solved():
            return 1

        if depth == 0:
            return 0

        moves = ['up', 'down', 'left', 'right']
        undo_moves = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
        if is_maximizing:
            best = float('-inf')
            for move in moves:
                if self.move(move):  # Apply the move and check if it's valid
                    value = self.alpha_beta(False, depth - 1, alpha, beta)
                    self.move(undo_moves[move])  # Undo the move
                    best = max(best, value)
                    alpha = max(alpha, best)
                    if alpha >= beta:
                        break
            return best
        else:
            best = float('inf')
            for move in moves:
                if self.move(move):  # Apply the move and check if it's valid
                    value = self.alpha_beta(True, depth - 1, alpha, beta)
                    self.move(undo_moves[move])  # Undo the move
                    best = min(best, value)
                    beta = min(beta, best)
                    if alpha >= beta:
                        break
            return best


def main():
    puzzle = Puzzle8()
    puzzle.fill_board()
    puzzle.display_board()
    print('#' * 50)
    puzzle.alpha_beta(True, 362_880)  # 9! = 362,880
    puzzle.display_board()


if __name__ == '__main__':
    main()
