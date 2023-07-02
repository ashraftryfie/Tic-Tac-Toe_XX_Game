import math


class GamePlay:

    counter_leaves = 0

    # evaluating the state
    def evaluate_state(self, state, spot, AI):

        if state.is_player_win(spot):
            if AI:
                return +math.inf
            else:
                return -math.inf

        evaluate_me = 0
        row = True
        column = True
        main_diagonal = True
        second_diagonal = True
        player = spot

        if AI:
            player = spot
        else:
            player = 'X' if spot == 'O' else 'O'

        # check rows
        for i in range(state.get_board_dimension()):
            for j in range(state.get_board_dimension()):
                if state.get_board()[i][j] == ('X' if player == 'O' else 'O'):
                    row = False
            if row:
                evaluate_me += 1
            row = True

        # check columns
        for i in range(state.get_board_dimension()):
            for j in range(state.get_board_dimension()):
                if state.get_board()[j][i] == ('X' if player == 'O' else 'O'):
                    column = False
            if column:
                evaluate_me += 1
            column = True

        # check main diagonal
        for i in range(state.get_board_dimension()):
            if state.get_board()[i][i] == ('X' if player == 'O' else 'O'):
                main_diagonal = False
            if main_diagonal:
                evaluate_me += 1
            main_diagonal = True

        # check second diagonal
        for i in range(state.get_board_dimension()):
            if state.get_board()[i][state.get_board_dimension() - 1 - i] == ('X' if player == 'O' else 'O'):
                second_diagonal = False
            if second_diagonal:
                evaluate_me += 1
            second_diagonal = True

        evaluate_opponent = 0
        row = True
        column = True
        main_diagonal = True
        second_diagonal = True

        # check rows
        for i in range(state.get_board_dimension()):
            for j in range(state.get_board_dimension()):
                if state.get_board()[i][j] == player:
                    row = False
            if row:
                evaluate_opponent += 1
            row = True

        # check columns
        for i in range(state.get_board_dimension()):
            for j in range(state.get_board_dimension()):
                if state.get_board()[j][i] == player:
                    column = False
            if column:
                evaluate_opponent += 1
            column = True

        # check main diagonal
        for i in range(state.get_board_dimension()):
            if state.get_board()[i][i] == player:
                main_diagonal = False
            if main_diagonal:
                evaluate_opponent += 1
            main_diagonal = True

        # check second diagonal
        for i in range(state.get_board_dimension()):
            if state.get_board()[i][state.get_board_dimension() - 1 - i] == player:
                second_diagonal = False
            if second_diagonal:
                evaluate_opponent += 1
            second_diagonal = True

        return evaluate_me - evaluate_opponent

    # secondary evaluate function
    def secondary_evaluate(self, state, spot, AI):
        if state.is_player_win(spot):
            if AI:
                score = -1
            else:
                score = +1
        else:
            score = 0

        return score

    # MiniMax Algorithm
    def MiniMax(self, state, depth, spot, AI):
        if AI:
            best = [-1, -1, +math.inf]
        else:
            best = [-1, -1, -math.inf]

        if depth == 0 or state.is_player_win(spot):
            self.counter_leaves += 1
            score = self.secondary_evaluate(state, spot, AI)
            print(self.counter_leaves)
            return [-1, -1, score]

        # next_states, cells_fixed = state.next_states('X' if spot == 'O' else 'O')
        next_states, cells_fixed = state.next_states('X')

        for cell in cells_fixed:
            x, y = cell[0], cell[1]
            state.get_board()[x][y] = spot
            # score = self.MiniMax(state, depth - 1, 'X' if spot == 'O' else 'O', not AI)
            score = self.MiniMax(state, depth - 1, 'X', not AI)
            state.get_board()[x][y] = '-'
            score[0], score[1] = x, y

            # if AI:
            #     if score[2] > best[2]:
            #         best = score  # max value
            # else:
            #     if score[2] < best[2]:
            #         best = score  # min value

            if AI:
                if score[2] < best[2]:
                    best = score  # min value
            else:
                if score[2] > best[2]:
                    best = score  # max value

        return best

    # optimize MiniMax algorithm with alpha beta pruning
    def alpha_beta(self, state, depth, spot, AI, alpha=-math.inf, beta=+math.inf):

        if depth == 0 or state.is_player_win(spot):
            score = self.evaluate_state(state, spot, AI)
            return [-1, -1, score]

        next_states, cells_fixed = state.next_states('X')

        if AI:
            best_score = [-1, -1, -math.inf]
            for cell in cells_fixed:
                x, y = cell[0], cell[1]
                state.get_board()[x][y] = spot
                score = self.alpha_beta(state, depth - 1, 'X', not AI, alpha, beta)
                state.get_board()[x][y] = '-'
                score[0], score[1] = x, y
                best_score = best_score if best_score[2] >= score[2] else score
                alpha = max(alpha, best_score[2])
                if beta <= alpha:
                    break

            return best_score

        else:
            best_score = [-1, -1, +math.inf]
            for cell in cells_fixed:
                x, y = cell[0], cell[1]
                state.get_board()[x][y] = spot
                score = self.alpha_beta(state, depth - 1, 'X' , not AI, alpha, beta)
                state.get_board()[x][y] = '-'
                score[0], score[1] = x, y
                best_score = best_score if best_score[2] <= score[2] else score
                beta = min(beta, best_score[2])
                if alpha >= beta:
                    break

            return best_score
