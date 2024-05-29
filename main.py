from typing import Dict


class GoGame:
    def __init__(self, size=9):
        self.ko = None
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.current_player = 'B'
        self.points = {"B": 0, "W": 0}
        self.pas = 0

    def change_player(self) -> None:
        self.current_player = "W" if self.current_player == "B" else "B"

    def print_board(self) -> None:
        for row in self.board:
            print("".join(row))
        print(self.points, self.ko)
        print()

    def is_on_board(self, x, y) -> bool:
        return 0<=x<self.size and 0<=y<self.size

    def place_stone(self, x, y) -> bool:
        if not self.is_on_board(x,y) or self.board[x][y] != "." or self.ko == (x,y):
            return False
        opponent = "W" if self.current_player == "B" else "B"
        self.ko = None
        self.board[x][y] = self.current_player
        if not self.has_liberty(x, y):
            for (nx, ny) in self.get_neighbors(x, y):
                if self.board[nx][ny] == opponent and not self.has_liberty(nx,ny):
                    self.change_player()
                    return True
            self.board[x][y] = "."
            return False
        self.remove_captured_stones(x,y)
        self.change_player()
        return True

    def remove_captured_stones(self, x, y) -> None:
        res = 0
        opponent = "W" if self.current_player == "B" else "B"
        for nx, ny in self.get_neighbors(x, y):
            if self.board[nx][ny]==opponent:
                if not self.has_liberty(nx, ny):
                    res += self.capture_group(nx, ny)
                    last = (nx,ny)
        self.points[self.current_player] += res
        if res == 1:
            self.ko = last

    def has_liberty(self, x, y) -> bool:
        visited = set()
        return self._has_liberty(x, y, visited)

    def _has_liberty(self, x, y, visited) -> bool:
        if (x,y) in visited:
            return False
        visited.add((x,y))
        for nx, ny in self.get_neighbors(x, y):
            if self.board[nx][ny] == ".":
                return True
            if self.board[nx][ny] == self.board[x][y] and self._has_liberty(nx, ny, visited):
                return True
        return False

    def get_neighbors(self, x, y) -> (int,int):
        neighbors = []
        if x > 0: neighbors.append((x - 1, y))
        if x < self.size - 1: neighbors.append((x + 1, y))
        if y > 0: neighbors.append((x, y - 1))
        if y < self.size - 1: neighbors.append((x, y + 1))
        return neighbors

    def capture_group(self, x, y) -> int:
        res = 0
        to_capture = [(x,y)]
        color = self.board[x][y]
        while to_capture:
            cx, cy = to_capture.pop()
            if self.board[cx][cy] == color:
                self.board[cx][cy] = "."
                res += 1
                to_capture.extend((nx, ny) for (nx, ny) in self.get_neighbors(cx, cy) if self.board[nx][ny] == color)
        return res

    def count_points(self) -> Dict[str, int]:
        result = self.points.copy()
        visited = set()

        def explore_territory(x, y):
            territory = []
            border_colors = set()
            to_explore = [(x, y)]
            while to_explore:
                cx, cy = to_explore.pop()
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                territory.append((cx, cy))
                for nx, ny in self.get_neighbors(cx, cy):
                    if self.board[nx][ny] == '.':
                        if (nx, ny) not in visited:
                            to_explore.append((nx, ny))
                    else:
                        border_colors.add(self.board[nx][ny])
            return territory, border_colors

        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == '.' and (x, y) not in visited:
                    territory, border_colors = explore_territory(x, y)
                    if len(border_colors) == 1:
                        owner = border_colors.pop()
                        result[owner] += len(territory)
                    else:
                        raise ValueError()

        return result

    def print_score(self) -> None:
        print(self.points)


def play_game():
    game = GoGame()

    while True:
        game.print_board()
        move = input(f"Player {game.current_player}, enter your move (row col), pass or 'quit': ")
        if move == "pass":
            if game.pas == 1:
                game.print_board()
                try:
                    print(game.count_points())
                    game.print_score()
                    break
                except:
                    print("game not over")
                    game.change_player()
                    continue
            else:
                game.pas = 1
                game.change_player()
                continue
        game.pas = 0
        if move == "quit":
            break
        try:
            x, y = map(int, move.split())
            if not game.place_stone(x, y):
                print("Invalid move")
        except ValueError:
            print("Invalid input. Enter row and column numbers separated by space.")
    print("Game over")

play_game()
