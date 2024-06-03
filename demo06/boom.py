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
        self.marked = set()
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
            print("Invalid input. Please enter a number between 0 and {} for both row and column.".format(self.width - 1))
            return False
        if (x, y) in self.revealed:
            return True

        self.revealed.add((x, y))

        if self.board[y][x] == -1:
            print("BOOM! You hit a mine!")
            self.print_board()
            return False

        if self.board[y][x] == 0:
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.revealed:
                    self.reveal(nx, ny)

        self.print_board()
        return True

    def mark(self, x, y):

        if (x, y) not in self.revealed:
            if (x, y) in self.marked:
                self.marked.remove((x, y))
            else:
                self.marked.add((x, y))
            self.print_board()

    def print_board(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if (x, y) in self.revealed:
                    if self.board[y][x] == -1:
                        row += "* "
                    else:
                        row += str(self.board[y][x]) + " "
                elif (x, y) in self.marked:
                    row += "! "
                else:
                    row += ". "
            print(row)

    def is_game_over(self):

        total_tiles = self.width * self.height
        non_mine_tiles = total_tiles - len(self.mines)
        revealed_tiles = non_mine_tiles - len(self.revealed)
        return revealed_tiles == 0 or len(self.revealed) + len(self.mines) == total_tiles

    def play(self):
        while not self.is_game_over():
            self.print_board()
            command = input("Enter row and column to reveal (e.g., '0 0'), or 'mark' to toggle mine flag: ").lower()
            if command == 'mark':
                continue
            else:
                coords = command.split()
                if len(coords) == 2:
                    try:
                        x, y = int(coords[0]), int(coords[1])
                        if not self.reveal(x, y):
                            return
                    except ValueError:
                        print("Invalid input. Please enter integers for row and column.")
                        continue
                else:
                    print("Invalid input. Please enter both row and column.")

        print("Congratulations! You've revealed all non-mine tiles. You win!")


game = Minesweeper(5, 5, 5)
game.play()