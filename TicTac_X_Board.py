import copy
import random
from GamePlay import GamePlay


class GameBoard:

    # set the board
    def __init__(self, dimension):
        self.dimension = dimension
        self.board = []

        for i in range(dimension):
            row = []
            for j in range(dimension):
                row.append('-')
            self.board.append(row)

    # get board
    def get_board(self):
        return self.board

    # get board dimension
    def get_board_dimension(self):
        return self.dimension

    # start randomly
    def get_random_first_player(self):
        return random.randint(0, 1)

    # check if the player can put a spot in this cell
    def can_fix_spot(self, row, col):
        if row > self.dimension or col > self.dimension:
            return False
        if self.board[row][col] != '-':
            return False
        return True

    # put a spot in a cell
    def fix_spot(self, row, col, player):
        self.board[row][col] = player

    # check if any player has won
    def is_player_win(self, player):
        win = None

        # checking rows
        for i in range(self.dimension):
            win = True
            for j in range(self.dimension):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # checking columns
        for i in range(self.dimension):
            win = True
            for j in range(self.dimension):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        # checking main diagonals
        win = True
        for i in range(self.dimension):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        # checking second diagonals
        win = True
        for i in range(self.dimension):
            if self.board[i][self.dimension - 1 - i] != player:
                win = False
                break
        if win:
            return win
        return False

        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    # when the board is filled then it is a DRAW !
    def is_board_filled(self):
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    # swap the turn between the two players
    def swap_player_turn(self, player):
        return 'X' if player == 'O' else 'O'

    # display the board
    def display_board(self):

        print('-------------------------')
        for row in self.board:
            for cell in row:
                print(f'| { cell } |', end='')
            print('\n' + '-------------------------')

    # mapping between input and output
    def mapping(self, choice):
        temp_choice = choice - 1
        i = int(temp_choice / self.dimension)
        j = int(temp_choice % self.dimension)
        return [i, j]

    # Next Board
    # get the possible states from this state
    def next_states(self, player):
        next_states = []  # to store the next states of the current state
        cells_fixed = []  # to store the fixed cell in the every next state

        # check every cell if available to fix a spot
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.can_fix_spot(i, j):
                    temp = copy.deepcopy(self)
                    temp.fix_spot(i, j, player)
                    next_states.append(temp)
                    cells_fixed.append([i, j])

        return next_states, cells_fixed

    # play the game showing next states for every player
    # def play_showing_next_states(self):
    #     chosen_state = self
    #     player = 'X' if self.get_random_first_player() == 1 else 'O'
    #
    #     while True:
    #
    #         # # checking whether current player won or not
    #         if chosen_state.is_player_win('X' if player == 'O' else 'O'):
    #             print()
    #             chosen_state.display_board()
    #             print("\nPlayer " + 'X Wins !' if player == 'O' else '\nPlayer O Wins !')
    #             break
    #
    #         # checking whether the game is draw or not
    #         if chosen_state.is_board_filled():
    #             chosen_state.display_board()
    #             print("\nMatch Draw !")
    #             break
    #
    #         next_states, cells_fixed = chosen_state.next_states(player)
    #         state_no = 0
    #         print('\n*************************\n')
    #         print("Player " + player + " turn :\n")
    #         print("POSSIBLE MOVEMENTS :")
    #         for state in next_states:
    #             print('\n*************************')
    #             print('        STATE :', state_no)
    #             state_no += 1
    #             state.display_board()
    #
    #         # swap the turn
    #         player = self.swap_player_turn(player)
    #         chosen_state = next_states[int(input("\nChoose a state : "))]

    # play the game between two players

    def play_two_players(self):

        player = 'X' if self.get_random_first_player() == 1 else 'O'

        while True:
            print(f"Player {player} turn :\n")

            self.display_board()

            # taking user input
            row, col = list(
                map(int, input("\nEnter row and column numbers to fix spot : ").split()))
            print()

            while not self.can_fix_spot(row - 1, col - 1):
                print("Unavailable move !\n")
                print(f"Player {player} turn :\n")
                self.display_board()
                row, col = list(
                    map(int, input("\nEnter row and column numbers to fix spot : ").split()))
                print()

            # fixing the spot
            self.fix_spot(row - 1, col - 1, player)

            # checking whether current player is won or not
            if self.is_player_win(player):
                print(f"Player {player} wins the game!")
                break

            # checking whether the game is draw or not
            if self.is_board_filled():
                print("Match Draw!")
                break

            # swapping the turn
            player = self.swap_player_turn(player)

        # showing the final view of board
        print()
        self.display_board()

    # play with AI
    def play_with_AI(self):

        level = int(input('\nEnter Level : \n1 : Easy\n2 : Medium\n3 : Hard\n'))  # difficulty

        # spot = 'X' if self.get_random_first_player() == 1 else 'O'
        spot = 'X'
        turn = 'AI' if self.get_random_first_player() == 1 else 'Human'

        AI = GamePlay()

        while True:

            if turn == 'Human':
                print('--------------new turn--------------')
                print(turn)
                print(f"Player Human turn, your spot is {spot} :\n")

                self.display_board()

                # taking user input
                cell = self.mapping(int(input(f"\nEnter cell number to fix spot (1-{ pow(self.dimension, 2) }) : ")))
                print()

                while not self.can_fix_spot(cell[0], cell[1]):
                    print("Unavailable move !\n")
                    print(f"Player Human turn :\n")
                    self.display_board()
                    cell = self.mapping(int(input(f"\nEnter cell number to fix spot (1-{ pow(self.dimension, 2) }) : ")))

                    print()

                # fixing the spot
                self.fix_spot(cell[0], cell[1], spot)

                # checking whether current player is won or not
                if self.is_player_win(spot):
                    print(f"Player Human lose the game!")
                    break

                # checking whether the game is draw or not
                if self.is_board_filled():
                    print("Match Draw!")
                    break

                # swapping the turn
                # spot = self.swap_player_turn(spot)
                spot = 'X'
                turn = 'AI'

            # AI turn
            else:
                print('--------------new turn--------------')
                print(turn)
                if level == 1:
                    depth = 2
                elif level == 2:
                    depth = 3
                else:
                    depth = 9

                spot_fixed = AI.alpha_beta(self, depth, spot, AI=False)
                # spot_fixed = AI.MiniMax(self, depth, spot, AI=True)
                self.fix_spot(spot_fixed[0], spot_fixed[1], spot)

                # checking whether current player is won or not
                if self.is_player_win(spot):
                    print(f"Player AI lose the game!")
                    break

                # checking whether the game is draw or not
                if self.is_board_filled():
                    print("Match Draw!")
                    break

                # swapping the turn
                # spot = self.swap_player_turn(spot)
                spot = 'X'
                turn = 'Human'

        # showing the final view of board
        print()
        self.display_board()
