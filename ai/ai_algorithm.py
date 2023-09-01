from copy import deepcopy
import random
import time

from constants import DARK, LIGHT, ROWS, COLUMNS

eval_count = 0


def get_eval_count():
    return eval_count


def reset_eval_count():
    global eval_count
    eval_count = 0


def iterative_deepening(board_state, max_depth, player, time_limit=5, itr_limit=5000):
    best_move = None
    start_time = time.time()
    for depth in range(1, max_depth + 1, 2):  # run minimax function from depth 1 to max depth (2 ply)
        if time_limit and (time.time() - start_time) > time_limit:
            break
        eval_score, move = minimax_hard(board_state, depth, True, player, itr_limit)
        if move is not None:
            best_move = move

    return eval_score, best_move


def reset_history_table():
    global history_table
    history_table = {}


# Minimax with history heuristic
history_table = {}  # a dictionary to store the history scores for each move


def minimax_hard(board_state, depth, is_max_turn, player, itr_limit=5000, alpha=float('-inf'), beta=float('inf')):
    global eval_count
    enemy_player = DARK if player is LIGHT else LIGHT
    max_player = player if is_max_turn else enemy_player  # evaluate based on who is max_player

    # Find all possible moves for the current player (max/min)
    board_state.find_all_possible_moves(player)

    # If reached terminal/leaf node OR game over
    if depth == 0 or board_state.no_moves_left():
        eval_count += 1
        return evaluate_hard(board_state, max_player), None

    best_score = float('-inf') if is_max_turn else float('inf')
    best_move = None
    move_with_score = dict()

    # Move ordering based on their history heuristic score
    sorted_moves = sorted(find_moves(board_state), key=lambda m: history_table.get(m, 0), reverse=True)

    # Simulate each move and evaluate their board state, move is (start_sq, end_sq)
    for move in sorted_moves:
        board_copy = deepcopy(board_state)
        board_copy.move_piece(move)  # move piece based on its found all possible moves

        # If maximizing player
        if is_max_turn:
            if itr_limit is not None and eval_count > itr_limit:
                break
            eval_score, _ = minimax_hard(board_copy, depth - 1, False, enemy_player, itr_limit, alpha, beta)
            move_with_score[move] = eval_score
            best_score = max(best_score, eval_score)
            alpha = max(alpha, eval_score)
        else:  # minimizing player
            if itr_limit is not None and eval_count > itr_limit:
                break
            eval_score, _ = minimax_hard(board_copy, depth - 1, True, enemy_player, itr_limit, alpha, beta)
            best_score = min(best_score, eval_score)
            beta = min(beta, eval_score)

        if best_score == eval_score:
            best_move = move

        if alpha >= beta:
            break  # prune the rest of this branch

        # Update history table with the cutoff moves
        history_table[best_move] = history_table.get(best_move, 0) + 1

    eval_count += 1
    return best_score, best_move


def minimax_easy(board_state, depth, is_max_turn, player, itr_limit=None, alpha=float('-inf'), beta=float('inf')):
    global eval_count
    enemy_player = DARK if player is LIGHT else LIGHT
    max_player = player if is_max_turn else enemy_player  # evaluate based on who is max_player

    # Find all possible moves for the current player (max/min)
    board_state.find_all_possible_moves(player)

    # If reached terminal/leaf node OR game over
    if depth == 0 or board_state.no_moves_left():
        eval_count += 1
        return evaluate_easy(board_state, max_player), None

    best_score = float('-inf') if is_max_turn else float('inf')
    best_move = None
    move_with_score = dict()

    # Move ordering based on their history heuristic score
    sorted_moves = sorted(find_moves(board_state), key=lambda m: history_table.get(m, 0), reverse=True)

    # Simulate each move and evaluate their board state, move is (start_sq, end_sq)
    for move in sorted_moves:
        board_copy = deepcopy(board_state)
        board_copy.move_piece(move)  # move piece based on its found all possible moves

        # If maximizing player
        if is_max_turn:
            if itr_limit is not None and eval_count > itr_limit:
                break
            eval_score, _ = minimax_easy(board_copy, depth - 1, False, enemy_player, itr_limit, alpha, beta)
            move_with_score[move] = eval_score

            best_score = max(best_score, eval_score)
            alpha = max(alpha, eval_score)
        else:  # minimizing player
            if itr_limit is not None and eval_count > itr_limit:
                break
            eval_score, _ = minimax_easy(board_copy, depth - 1, True, enemy_player, itr_limit, alpha, beta)
            best_score = min(best_score, eval_score)
            beta = min(beta, eval_score)

        if best_score == eval_score:
            best_move = move

        if alpha >= beta:
            break  # prune the rest of this branch

        # Update history table with the cutoff moves
        history_table[best_move] = history_table.get(best_move, 0) + 1

    eval_count += 1
    return best_score, best_move


def minimax_medium(board_state, depth, is_max_turn, player, itr_limit=None, alpha=float('-inf'), beta=float('inf')):
    global eval_count
    enemy_player = DARK if player is LIGHT else LIGHT
    max_player = player if is_max_turn else enemy_player  # evaluate based on who is max_player

    # Find all possible moves for the current player (max/min)
    board_state.find_all_possible_moves(player)

    # If reached terminal/leaf node OR game over
    if depth == 0 or board_state.no_moves_left():
        eval_count += 1
        return evaluate_medium(board_state, max_player), None

    best_score = float('-inf') if is_max_turn else float('inf')
    best_move = None
    move_with_score = dict()

    # Move ordering based on their history heuristic score
    sorted_moves = sorted(find_moves(board_state), key=lambda m: history_table.get(m, 0), reverse=True)

    # Simulate each move and evaluate their board state, move is (start_sq, end_sq)
    for move in sorted_moves:
        board_copy = deepcopy(board_state)
        board_copy.move_piece(move)  # move piece based on its found all possible moves

        # If maximizing player
        if is_max_turn:
            if itr_limit is not None and eval_count > itr_limit:
                break
            eval_score, _ = minimax_medium(board_copy, depth - 1, False, enemy_player, itr_limit, alpha, beta)
            move_with_score[move] = eval_score

            best_score = max(best_score, eval_score)
            alpha = max(alpha, eval_score)
        else:  # minimizing player
            if itr_limit is not None and eval_count > itr_limit:
                break
            eval_score, _ = minimax_medium(board_copy, depth - 1, True, enemy_player, itr_limit, alpha, beta)
            best_score = min(best_score, eval_score)
            beta = min(beta, eval_score)

        if best_score == eval_score:
            best_move = move

        if alpha >= beta:
            break  # prune the rest of this branch

        # Update history table with the cutoff moves
        history_table[best_move] = history_table.get(best_move, 0) + 1

    eval_count += 1
    return best_score, best_move


# Minimax with alpha-beta pruning
def minimax_alpha_beta(board_state, depth, is_max_turn, player, alpha=float('-inf'),
                       beta=float('inf')):
    global eval_count
    enemy_player = DARK if player is LIGHT else LIGHT
    max_player = player if is_max_turn else enemy_player

    # Find all possible moves for the current player (max/min)
    board_state.find_all_possible_moves(player)

    # If reached terminal/leaf node OR game over
    if depth == 0 or board_state.no_moves_left():  # or game over/winner found  # when reach leaf/terminal node, evaluate it
        eval_count += 1
        return evaluate(board_state, max_player), None  # return evaluate(board_state, player)

    best_score = float('-inf') if is_max_turn else float('inf')
    best_moves = []
    best_move = None

    # Find all possible moves for the current player (max/min) and order them based on captures
    # if board_state.capture_possible:
    #     moves = sorted(board_state), key=lambda move: len(board_state.get_captures(player, move)))

    # Simulate each move and evaluate their board state, move is (start_sq, end_sq)
    for move in find_moves(board_state):
        board_copy = deepcopy(board_state)
        board_copy.move_piece(move)  # move piece based on its found all possible moves

        # If maximizing player
        if is_max_turn:
            eval_score, _ = minimax(board_copy, depth - 1, False, enemy_player, alpha, beta)
            best_score = max(best_score, eval_score)
            alpha = max(alpha, eval_score)
        else:  # minimizing player
            eval_score, _ = minimax(board_copy, depth - 1, True, enemy_player, alpha, beta)
            best_score = min(best_score, eval_score)
            beta = min(beta, eval_score)

        if best_score == eval_score:
            best_moves.append(move)

        if alpha >= beta:
            break  # prune the rest of this branch

    # Random move among all best moves
    if best_moves:
        print("Possible MOVES")
        best_move = random.choice(best_moves)  # randomly pick one of the best moves

    eval_count += 1
    return best_score, best_move


def minimax_pure_code_simplified(board_state, depth, is_max_turn,
                                 player):
    global eval_count
    enemy_player = DARK if player is LIGHT else LIGHT
    max_player = player if is_max_turn else enemy_player

    if depth == 0:
        eval_count += 1
        return evaluate_hard(board_state, max_player), None

    best_score = float('-inf') if is_max_turn else float('inf')
    best_moves = []
    best_move = None

    # Find all possible moves for the current player (max/min)
    board_state.find_all_possible_moves(player)

    # Simulate each move and evaluate their board state, move is (start_sq, end_sq)
    for move in find_moves(board_state):
        board_copy = deepcopy(board_state)
        board_copy.move_piece(move)  # move piece based on its found all possible moves

        if is_max_turn:
            eval_score, _ = minimax(board_copy, depth - 1, False, enemy_player)
            best_score = max(best_score, eval_score)
        else:
            eval_score, _ = minimax(board_copy, depth - 1, True, enemy_player)
            best_score = min(best_score, eval_score)

        if best_score == eval_score:
            best_moves.append(move)

    # If moves still exist,
    if best_moves:
        print("Possible MOVESS")
        best_move = random.choice(best_moves)  # randomly pick one of the best moves
    else:
        print("No possible MOVESS")

    eval_count += 1
    return best_score, best_move


def minimax_pure(board_state, depth, is_max, player):
    global eval_count
    if player is LIGHT:
        enemy_player = DARK

    else:
        enemy_player = LIGHT

    if is_max:
        max_player = player
    else:
        max_player = enemy_player

    if depth == 0:
        eval_count += 1
        return evaluate_hard(board_state, max_player), None

    if is_max:
        max_eval = float('-inf')
        best_move = None
        best_moves = []

        board_state.find_all_possible_moves(player)

        move_with_score = dict()

        # return board state after moving and evaluate it, move is (start_sq, end_sq)
        for move in find_moves(board_state):
            board_copy = deepcopy(board_state)
            # board_copy = board_state.create_copy()  #if use this way, then no nid find_all... cos done in init
            board_copy.move_piece(move)  # move piece based on its found all possible moves
            eval_score, _ = minimax(board_copy, depth - 1, False, enemy_player)
            move_with_score[move] = eval_score
            print(move_with_score)

            max_eval = max(max_eval, eval_score)
            if max_eval == eval_score:
                best_moves.append(move)
                best_move = move

        if best_moves:
            print("possible MOVESS")

            # best_move = random.choice(best_moves)  # randomly pick one of the best moves
        else:
            # best_move = None
            print("No possible MOVESS")

        eval_count += 1
        return max_eval, best_move

    else:

        min_eval = float('inf')
        best_move = None
        best_moves = []

        board_state.find_all_possible_moves(player)
        for move in find_moves(board_state):
            board_copy = deepcopy(board_state)
            board_copy.move_piece(move)  # move piece based on its found all possible moves
            eval_score, current_move = minimax(board_copy, depth - 1, True, enemy_player)
            min_eval = min(min_eval, eval_score)
            if min_eval == eval_score:
                best_moves.append(move)
                best_move = move

        if best_moves:
            print("possible MOVESS")

            # best_move = random.choice(best_moves)  # randomly pick one of the best moves
        else:
            # best_move = None
            print("No possible MOVESS")

        eval_count += 1
        return min_eval, best_move


def find_moves(board_state):
    moves = []
    for start_sq, end_sq_dict in board_state.all_possible_moves.items():
        for end_sq in end_sq_dict.keys():
            moves.append((start_sq, end_sq))
    return moves  # [(start_sq1, end_sq1), (start_sq2, end_sq2), ...]


def evaluate_hard(board, max_player):
    eval_score = 0
    piece_count_weight = 1
    capture_weight = 3
    mobility_weight = 2

    if board.no_moves_left():  # You lost
        eval_score += float('-inf') if board.turn is max_player else float('inf')

    piece_count_score = 0
    if max_player is LIGHT:
        piece_count_score = piece_count_weight * (board.light_pieces - board.dark_pieces +
                                                  (board.light_kings - board.dark_kings) * 3)
    elif max_player is DARK:
        piece_count_score = piece_count_weight * (board.dark_pieces - board.light_pieces +
                                                  (board.dark_kings - board.light_kings) * 3)
    eval_score += piece_count_score

    if board.capture_possible:
        if board.turn is max_player:
            eval_score += capture_weight
        else:
            eval_score -= capture_weight

    # Mobility
    num_moves = len(find_moves(board))
    if board.turn == max_player:  # If max player turn
        eval_score += mobility_weight * num_moves
    else:  # If min player turn
        eval_score -= mobility_weight * num_moves

    positional_weights = [
        [0, 3, 0, 3, 0, 3, 0, 3],
        [2, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 2],
        [2, 0, 4, 0, 4, 0, 1, 0],
        [0, 1, 0, 4, 0, 4, 0, 2],
        [2, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 2],
        [3, 0, 3, 0, 3, 0, 3, 0]
    ]

    # Evaluating the pieces
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (row + col) % 2 == 0:  # Skip if WHITE squares
                continue
            square = board.get_square((row, col))
            piece = square.get_piece()
            if piece is not None:
                piece_colour = piece.get_colour()

                # Positional value
                pos_value = positional_weights[row][col] * piece.get_value()
                if piece_colour == max_player:
                    eval_score += pos_value
                else:
                    eval_score -= pos_value

                # Defensive strength
                num_defenders = find_num_defenders(board, square)
                if piece_colour == max_player:
                    eval_score += num_defenders * piece.get_value()
                else:
                    eval_score -= num_defenders * piece.get_value()

                # Vulnerability
                num_attackers = find_num_attackers(board, square)
                if piece_colour == max_player:
                    # Higher penalty for vulnerability compared to defensive
                    eval_score -= 2 * num_attackers * piece.get_value()
                    if num_attackers > 1:
                        eval_score -= 2  # Fixed penalty
                else:
                    eval_score += 2 * num_attackers * piece.get_value()
                    if num_attackers > 1:
                        eval_score += 2

        # Prevent AI same at each other
        num_pieces = board.light_pieces + board.dark_pieces
        num_kings = board.dark_kings + board.light_kings
        if num_kings >= num_pieces:
            random_num = random.randint(1, 3)
            eval_score += random_num

    return eval_score


def evaluate_medium(board, max_player):
    eval_score = 0
    piece_count_weight = 1
    capture_weight = 3
    mobility_weight = 2

    if board.no_moves_left():  # You lost
        eval_score += float('-inf') if board.turn is max_player else float('inf')

    piece_count_score = 0
    if max_player is LIGHT:
        piece_count_score = piece_count_weight * (board.light_pieces - board.dark_pieces +
                                                  (board.light_kings - board.dark_kings) * 3)
    elif max_player is DARK:
        piece_count_score = piece_count_weight * (board.dark_pieces - board.light_pieces +
                                                  (board.dark_kings - board.light_kings) * 3)
    eval_score += piece_count_score

    if board.capture_possible:
        if board.turn is max_player:
            eval_score += capture_weight
        else:
            eval_score -= capture_weight

    # Mobility
    num_moves = len(find_moves(board))
    if board.turn == max_player:  # If max player turn
        eval_score += mobility_weight * num_moves
    else:  # If min player turn
        eval_score -= mobility_weight * num_moves

    positional_weights = [
        [0, 3, 0, 3, 0, 3, 0, 3],
        [2, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 2],
        [2, 0, 4, 0, 4, 0, 1, 0],
        [0, 1, 0, 4, 0, 4, 0, 2],
        [2, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 2],
        [3, 0, 3, 0, 3, 0, 3, 0]
    ]

    # Evaluating the pieces
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (row + col) % 2 == 0:  # Skip if WHITE squares
                continue
            square = board.get_square((row, col))
            piece = square.get_piece()
            if piece is not None:
                piece_colour = piece.get_colour()

                # Positional value
                pos_value = positional_weights[row][col] * piece.get_value()
                if piece_colour == max_player:
                    eval_score += pos_value
                else:
                    eval_score -= pos_value

        # Prevent AI same at each other
        num_pieces = board.light_pieces + board.dark_pieces
        num_kings = board.dark_kings + board.light_kings
        if num_kings >= num_pieces:
            random_num = random.randint(1, 3)
            eval_score += random_num

    return eval_score


def evaluate_easy(board, max_player):
    eval_score = 0
    piece_count_weight = 1

    if board.no_moves_left():  # You lost
        eval_score += float('-inf') if board.turn is max_player else float('inf')

    piece_count_score = 0
    if max_player is LIGHT:
        piece_count_score = piece_count_weight * (board.light_pieces - board.dark_pieces +
                                                  (board.light_kings - board.dark_kings) * 3)
    elif max_player is DARK:
        piece_count_score = piece_count_weight * (board.dark_pieces - board.light_pieces +
                                                  (board.dark_kings - board.light_kings) * 3)
    eval_score += piece_count_score

    positional_weights = [
        [0, 3, 0, 3, 0, 3, 0, 3],
        [2, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 2],
        [2, 0, 4, 0, 4, 0, 1, 0],
        [0, 1, 0, 4, 0, 4, 0, 2],
        [2, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 2],
        [3, 0, 3, 0, 3, 0, 3, 0]
    ]

    # Evaluating the pieces
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (row + col) % 2 == 0:  # Skip if WHITE squares
                continue
            square = board.get_square((row, col))
            piece = square.get_piece()
            if piece is not None:
                piece_colour = piece.get_colour()

                # Positional value
                pos_value = positional_weights[row][col] * piece.get_value()
                if piece_colour == max_player:
                    eval_score += pos_value
                else:
                    eval_score -= pos_value

        # Prevent AI same at each other
        num_pieces = board.light_pieces + board.dark_pieces
        num_kings = board.dark_kings + board.light_kings
        if num_kings >= num_pieces:
            random_num = random.randint(1, 3)
            eval_score += random_num

    return eval_score


def find_num_defenders(board, square):
    num_defenders = 0
    for neighbor in square.find_neighbours():
        neighbor_sq = board.get_square(neighbor)
        if neighbor_sq.get_piece() and neighbor_sq.get_piece_colour() == square.get_piece_colour():
            num_defenders += 1
    return num_defenders


def find_num_attackers(board, square):
    num_attackers = 0
    for neighbor in square.find_neighbours():
        neighbor_sq = board.get_square(neighbor)
        if neighbor_sq.get_piece() and neighbor_sq.get_piece_colour() != square.get_piece_colour():
            num_attackers += 1
    return num_attackers
