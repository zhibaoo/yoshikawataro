from kogi_canvas import play_othello

BLACK=1
WHITE=2

board = [
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,1,2,0,0],
        [0,0,2,1,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
]

#play_othello(TaroAI())

import math

BLACK = 1
WHITE = 2

def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False

def get_legal_moves(board, stone):
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                moves.append((x, y))
    return moves

def simulate_place(board, stone, x, y):
    board[y][x] = stone
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        stones_to_flip = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy

        if stones_to_flip and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            for fx, fy in stones_to_flip:
                board[fy][fx] = stone

def evaluate_board(board, stone):
    stable_discs = 0
    mobility = 0
    potential_mobility = 0
    corner_positions = [(0, 0), (0, 5), (5, 0), (5, 5)]
    bad_positions = [(0, 1), (1, 0), (4, 0), (5, 1), (0, 4), (1, 5), (4, 5), (5, 4)]

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                if (x, y) in corner_positions:
                    stable_discs += 300
                elif (x, y) in bad_positions:
                    stable_discs -= 150
                else:
                    stable_discs += 1
            elif board[y][x] == 3 - stone:
                if (x, y) in corner_positions:
                    stable_discs -= 300
                elif (x, y) in bad_positions:
                    stable_discs += 150
                else:
                    stable_discs -= 1

    # モビリティの評価
    my_moves = len(get_legal_moves(board, stone))
    opponent_moves = len(get_legal_moves(board, 3 - stone))
    mobility = (my_moves - opponent_moves) * 30  # モビリティの重みをさらに強化

    # 潜在モビリティの評価
    potential_mobility = sum(
        1 for y in range(len(board)) for x in range(len(board[0]))
        if board[y][x] == 0 and any(
            0 <= x + dx < len(board[0]) and 0 <= y + dy < len(board) and can_place_x_y(board, 3 - stone, x + dx, y + dy)
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        )
    )

    # 石数を終盤で評価
    total_stones = sum(row.count(BLACK) + row.count(WHITE) for row in board)
    stone_count_bonus = 0
    if total_stones > 50:
        stone_count_bonus = sum(row.count(stone) for row in board) * 10

    return stable_discs + mobility - potential_mobility * 5 + stone_count_bonus
  
def place(self, board, stone):
    depth = self.determine_depth(board)
    _, best_move = self.alpha_beta(board, stone, depth, -math.inf, math.inf, True)
    print(f"AIが選択した手: {best_move} (評価値: {_})")
    return best_move

class TaroAI:
    def face(self):
        return "💪"

    def place(self, board, stone):
        depth = self.determine_depth(board)
        _, best_move = self.alpha_beta(board, stone, depth, -math.inf, math.inf, True)
        return best_move

    def determine_depth(self, board):
        """局面に応じた探索深度を設定"""
        total_stones = sum(row.count(BLACK) + row.count(WHITE) for row in board)
        if total_stones < 20:
            return 4  # 序盤
        elif total_stones < 50:
            return 8  # 中盤
        else:
            return 14  # 終盤（完全読み）

    def alpha_beta(self, board, stone, depth, alpha, beta, maximizing):
        legal_moves = get_legal_moves(board, stone)
        if depth == 0 or not legal_moves:
            return evaluate_board(board, stone), None

        best_move = None

        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                x, y = move
                simulated_board = [row[:] for row in board]
                simulate_place(simulated_board, stone, x, y)
                eval, _ = self.alpha_beta(simulated_board, 3 - stone, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in legal_moves:
                x, y = move
                simulated_board = [row[:] for row in board]
                simulate_place(simulated_board, stone, x, y)
                eval, _ = self.alpha_beta(simulated_board, 3 - stone, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

play_othello(TaroAI())
