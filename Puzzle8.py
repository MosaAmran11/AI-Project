import tkinter as tk
import heapq
import random


class Puzzle8:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.numbers = [f'{i}' for i in range(1, 9)]  # Form 1 to 8
        self.numbers.append(' ')  # Add a blank slot for moving
        self.moves = ['up', 'down', 'left', 'right']
        self.undo_moves = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}

    def fill_board(self, fill: list = None):
        if fill is not None:
            self.board = fill
            return None
        list_of_nums = list(self.numbers)
        for row in range(3):
            for col in range(3):
                item = random.choice(list_of_nums)  # Take a random value
                self.board[row][col] = item  # Add the chosen value to the board
                list_of_nums.remove(item)  # Remove the chosen value from the list to avoid choosing it again

    def display_board(self):
        for row in self.board:
            print(' | '.join(row))
            print('-' * 9)

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

    def manhattan_distance(self):
        goal_positions = {
            '1': (0, 0), '2': (0, 1), '3': (0, 2),
            '8': (1, 0), ' ': (1, 1), '4': (1, 2),
            '7': (2, 0), '6': (2, 1), '5': (2, 2)
        }
        distance = 0
        for row in range(3):
            for col in range(3):
                value = self.board[row][col]
                goal_row, goal_col = goal_positions[value]
                distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def a_star(self):
        def reconstruct_path(came_from, current):
            path = []
            while current in came_from:
                current, move = came_from[current]
                path.append(move)
            return path[::-1]

        start = tuple(tuple(row) for row in self.board)
        goal = (
            ('1', '2', '3'),
            ('8', ' ', '4'),
            ('7', '6', '5')
        )
        queue = []
        heapq.heappush(queue, (0, start))
        came_from = {}
        g_score = {start: 0}  # g(n) = The actual cost to reach the node
        f_score = {start: self.manhattan_distance()}  # f(n) = g(n) + h(n)

        while queue:
            _, current_board = heapq.heappop(queue)

            if current_board == goal:
                return reconstruct_path(came_from, current_board)

            blank_position = None
            for row_index, row in enumerate(current_board):
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

            for move, (new_row, new_col) in moves.items():
                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    new_board = [list(row) for row in current_board]  # Convert from tuple to list

                    # Swap the blank slot with the new position
                    new_board[row][col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[row][col]
                    new_board = tuple(tuple(row) for row in new_board)  # Convert from list to tuple

                    temp_g_score = g_score[current_board] + 1

                    if new_board not in g_score or temp_g_score < g_score[new_board]:
                        came_from[new_board] = (current_board, move)
                        g_score[new_board] = temp_g_score
                        f_score[new_board] = temp_g_score + self.manhattan_distance()
                        heapq.heappush(queue, (f_score, new_board))
        return None


class PuzzleGUI:
    def __init__(self, root, puzzle: Puzzle8):
        self.root = root
        self.puzzle = puzzle
        self.solution = puzzle.a_star()
        while self.solution is None:
            self.puzzle.fill_board()
            self.puzzle.display_board()
            self.solution = self.puzzle.a_star()
        print(f'{len(self.solution) = }')
        self.step_index = 0

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                button = tk.Button(root, text=self.puzzle.board[row][col], font=('Helvetica', 20), width=4, height=2)
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

        self.next_button = tk.Button(root, text="Next", command=self.next_step)
        self.next_button.grid(row=3, column=2)
        self.prev_button = tk.Button(root, text="Previous", command=self.prev_step)
        self.prev_button.grid(row=3, column=0)
        self.steps_label = tk.Label(root, text=f'{self.step_index}/{len(self.solution)}')
        self.steps_label.grid(row=3, column=1)

    def update_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=self.puzzle.board[row][col])
        self.steps_label.config(text=f'{self.step_index}/{len(self.solution)}')

    def next_step(self):
        if self.step_index < len(self.solution):
            move = self.solution[self.step_index]
            self.puzzle.move(move)
            self.step_index += 1
            self.update_board()

    def prev_step(self):
        if self.step_index > 0:
            self.step_index -= 1
            move = self.solution[self.step_index]
            self.puzzle.move(self.puzzle.undo_moves[move])
            self.update_board()


def main():
    puzzle = Puzzle8()
    puzzle.fill_board()
    root = tk.Tk()
    gui = PuzzleGUI(root, puzzle)
    root.mainloop()
    # puzzle.display_board()
    # print('#' * 50)
    # path = puzzle.a_star()
    # if path:
    #     print('Solution found:')
    #     print(' -> '.join(path))
    #     for move in path:
    #         puzzle.move(puzzle.undo_moves[move])
    #         puzzle.display_board()
    #         print()
    # else:
    #     print('No solution found')


if __name__ == '__main__':
    main()
