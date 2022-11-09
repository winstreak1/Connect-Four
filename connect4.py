# Python Final Project
# Connect Four
#
# Erik Ackermann
# Charlene Wang
#
# Connect 4 Module
# February 27, 2012
# Accessed and revised by Peter Mavronicolas Nov. 8,2022


import os
from minimax import Minimax
import random
import time


class Game(object):
    """ Game object that holds state of Connect 4 board and game values
    """
    # initialize variables
    board = None
    round = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    game_name = u"Connecter Four in AI"  # U+2122 is "tm" this is a joke
    colors = ["x", "o"]

    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = None


        # do cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        print(u"Welcome to {0}!".format(self.game_name))

        #default to computer and name as bot1
        while self.players[0] == None:
            choice = str("C")
            if choice == "Computer" or choice.lower() == "c":
                name = str("Bot1")
                diff = int(input("Enter difficulty for Bot1 (1 - 4) "))
                self.players[0] = AIPlayer(name, self.colors[0], diff + 1)
            else:
                print("Invalid choice, please try again")
        print("{0} will be {1}".format(self.players[0].name, self.colors[0]))

        #default to computer and name as bot2
        while self.players[1] == None:
            choice = str("C")
            if choice == "Computer" or choice.lower() == "c":
                name = str("Bot2")
                diff = int(input("Enter difficulty for Bot2 (1 - 4) "))
                self.players[1] = AIPlayer(name, self.colors[1], diff + 1)
            else:
                print("Invalid choice, please try again")
        print("{0} will be {1}".format(self.players[1].name, self.colors[1]))

        # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]
        # initialize array and nested for loop through entire board
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')
    # initialize new game
    def newGame(self):
        """ Function to reset the game, but not the names or colors
        """
        self.round = 1
        self.finished = False
        self.winner = None

        # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]

        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')
    # function to change turns
    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        # increment the round
        self.round += 1

    def nextMove(self):
        player = self.turn

        # 7 x 6 = 42 legal places for pieces on the board
        # exactly one piece is added to the board each turn
        if self.round > 42:
            self.finished = True
            # this would be a stalemate :(
            return

        # move is the column that player want's to play
        move = player.move(self.board)
        # loop to call several functions determining placement of game piece
        for i in range(6):
            if self.board[i][move] == ' ':
                self.board[i][move] = player.color
                self.switchTurn()
                self.checkForFours()
                self.printState()
                return

        # if we get here, then the column is full
        print("Invalid move (column is full)")
        return
    # function to specifically check for a streak of four
    def checkForFours(self):
        # nested for loop iterating through entire board both vert. and horiz.
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.finished = True
                        return

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.finished = True
                        return

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        print(slope)
                        self.finished = True
                        return
    # function to iterate vertically through board
    def verticalCheck(self, row, col):
        # print("checking vert")
        fourInARow = False
        consecutiveCount = 0

        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
        # conditional statement checking for 4 win streak or connect four
        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow

    # function to iterate horizontally through board
    def horizontalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0

        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow
    # function to check for diagonal connect four
    def diagonalCheck(self, row, col):
        fourInARow = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented
        # conditional statements for positive slope check
        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope begining off the board
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is decremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope
    # function to search for beginning of connect four
    def findFours(self):
        # nested loop to iterate through board checking for pieces already placed
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.highlightFour(i, j, 'vertical')

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.highlightFour(i, j, 'horizontal')

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        self.highlightFour(i, j, 'diagonal', slope)
    # function to chnage piece from lower to capital letters
    def highlightFour(self, row, col, direction, slope=None):
        #conditional statements
        if direction == 'vertical':
            for i in range(4):
                self.board[row + i][col] = self.board[row + i][col].upper()
        #else if
        elif direction == 'horizontal':
            for i in range(4):
                self.board[row][col + i] = self.board[row][col + i].upper()
        #else if
        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.board[row + i][col + i] = self.board[row + i][col + i].upper()
            # else if
            elif slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.board[row - i][col + i] = self.board[row - i][col + i].upper()

        else:
            print("Error - Cannot enunciate four-of-a-kind")
    # function to build board
    def printState(self):
        # cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        print(u"{0}!".format(self.game_name))
        print("Round: " + str(self.round))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner")
            else:
                print("Game was a draw")


class Player(object):
    """ Player object.  This class is for human players.
    """

    type = None  # possible types are "Human" and "AI"
    name = None
    color = None

    def __init__(self, name, color):
        self.type = "Human"
        self.name = name
        self.color = color

    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        column = None
        while column == None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Invalid choice, try again")
        return column

# class for AI or computer player to make decisions
class AIPlayer(Player):

    difficulty = None
    # function to initialize variables
    def __init__(self, name, color, difficulty=5):
        self.type = "AI"
        self.name = name
        self.color = color
        self.difficulty = difficulty

    # function to move player based on random function
    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))

        # sleeping for about 1 second makes it looks like he's thinking
        # time.sleep(random.randrange(8, 17, 1)/10.0)
        # return random.randint(0, 6)

        m = Minimax(state)
        best_move, value = m.alphaBeta(self.difficulty, state, self.color)
        return best_move



