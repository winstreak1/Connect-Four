# Python Final Project
# Connect Four
# Erik Ackermann
# Charlene Wang
# Connect 4 Module
# February 27, 2012
# Accessed and revised by Peter Mavronicolas Nov. 8,2022

import random

# minimax algorith as a class
class Minimax(object):
    """ Minimax object that takes a current connect four board state
    """
    # declare variables
    board = None
    pieces = ["x", "o"]

    # function to initialize the game board and piece 'x'
    def __init__(self, board):
        # copy the board to self.board
        self.board = [x[:] for x in board]

    # function to assign alpha beta algorithm
    def alphaBeta(self, depth, state, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """

        # determine opponent's piece
        if curr_player == self.pieces[0]:
            opp_player = self.pieces[1]
        else:
            opp_player = self.pieces[0]

        # enumerate all legal moves
        legal_moves = {}  # will map legal move states to their alpha values
        for col in range(7):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, col, curr_player)
                legal_moves[col] = -self.search(depth - 1, temp, opp_player)

        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

    def search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever
            called this search

            Returns the alpha value
        """

        # loop w/ conditional statement for legal moves
        legal_moves = []
        for i in range(7):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)

        # conditional for bot1 and bot2 pieces
        if curr_player == self.pieces[0]:
            opp_player = self.pieces[1]
        else:
            opp_player = self.pieces[0]

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth - 1, child, opp_player))
        return alpha
    # function w/ boolean if move is legal
    def isLegalMove(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """

        for i in range(6):
            if state[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True

        # if we get here, the column is full
        return False
    # ends game if either bot1 or bot2 wins
    def gameIsOver(self, state):
        if self.checkForStreak(state, self.pieces[0], 4) >= 1:
            return True
        elif self.checkForStreak(state, self.pieces[1], 4) >= 1:
            return True
        else:
            return False
    #function to move the players piece
    def makeMove(self, state, column, piece):
        """ Change a state object to reflect a player, denoted by piece,
            making a move at column 'column'

            Returns a copy of new state array with the added move
        """
        # for loop that stores temporary location that is empty and replaced by piece
        temp = [x[:] for x in state]
        for i in range(6):
            if temp[i][column] == ' ':
                temp[i][column] = piece
                return temp
    # assigns name to streak of either 2,3,4 bot1 or bot2
    def value(self, state, piece):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 +
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if piece == self.pieces[0]:
            o_piece = self.pieces[1]
        else:
            o_piece = self.pieces[0]

        my_fours = self.checkForStreak(state, piece, 4)
        my_threes = self.checkForStreak(state, piece, 3)
        my_twos = self.checkForStreak(state, piece, 2)
        opp_fours = self.checkForStreak(state, o_piece, 4)
        #opp_threes = self.checkForStreak(state, o_piece, 3)
        #opp_twos = self.checkForStreak(state, o_piece, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours * 100000 + my_threes * 100 + my_twos
    # i as rows and j as columns in 2d array
    def checkForStreak(self, state, piece, streak):
        count = 0
        # nested for loop 
        for i in range(6):
            for j in range(7):
                #conditional statement if pieces equal one another vert and horiz.
                if state[i][j].lower() == piece.lower():
                    # check if a vertical streak starts at (i, j)
                    count += self.verticalStreak(i, j, state, streak)

                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.horizontalStreak(i, j, state, streak)

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self.diagonalCheck(i, j, state, streak)
        # return the sum of streaks of length 'streak'
        return count
    # function to loop through rows, i
    def verticalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for i in range(row, 6):
            if state[i][col].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    # function to loop through columns, j
    def horizontalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for j in range(col, 7):
            if state[row][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    # function to ccheck diagonal streak
    def diagonalCheck(self, row, col, state, streak):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented
        # conditional statement returning total
        if consecutiveCount >= streak:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        return total
