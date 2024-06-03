import random


class Minesweeper:
    def __init__(self, width=5, height=5, mines=10):
        if mines > width * height:
            raise ValueError("Too many mines for the board size.")
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.mines = set()
        self.revealed = set()
        self.place_mines(mines)

    def place_mines(self, mine_count):
        while len(self.mines) < mine_count:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if (x, y) not in self.mines:
                self.mines.add((x, y))
                self.board[y][x] = -1


        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.mines:
                    count = 0
                    for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) in self.mines:
                            count += 1
                    self.board[y][x] = count

    def reveal(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            print(
                "Invalid input. Please enter a number between 0 and {} for both row and column.".format(self.width - 1))
            return False
        if (x, y) in self.revealed or (x, y) in self.mines:
            return

        self.revealed.add((x, y))

        if self.board[y][x] == -1:
            print("BOOM! You hit a mine!")
            self.print_board()
            return False

        if self.board[y][x] == 0:
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.revealed:
                    if not self.reveal(nx, ny):
                        return False

        return True

    def print_board(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if (x, y) in self.revealed:
                    row += str(self.board[y][x]) + " "
                else:
                    row += "." + " "
            print(row)

        # 示例用法


game = Minesweeper(5, 5, 5)
while True:
    game.print_board()
    user_input = input("Enter row and column (e.g., 0 0 for top-left corner): ").split()
    if len(user_input) != 2:
        print("Invalid input. Please enter both row and column.")
        continue
    try:
        x, y = int(user_input[0]), int(user_input[1])
    except ValueError:
        print("Invalid input. Please enter integers for row and column.")
        continue
    if not game.reveal(x, y):
        break