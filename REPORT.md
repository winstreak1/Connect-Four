# Connect-Four

    Peter G. Mavronicolas
    CS 580, Fall 2022
    Dr. Yaohang Li
    Nov. 8, 2022

## Introduction
Connect-Four is a program that utilizes artificial intelligence; specifically the algorithms minimax and alpha-beta while playing the popular game of Connect Four. The original source code provided by 
Erik Ackermann was modified by setting the gameplay parameters to computer vs. computer play. The user still has the option to choose from levels 1-4 for each player which can drastically alter the results of the game. 
Any modifications to the algorithm can be made in the file named minimax.py, class minimax().
## Code

### connect4.py
```commandline
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
        time.sleep(random.randrange(8, 17, 1)/10.0)
        return random.randint(0, 6)

        m = Minimax(state)
        best_move, value = m.alphaBeta(self.difficulty, state, self.color)
        return best_move

```

### minimax.py
```commandline
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

```

### play.py
```commandline
from connect4 import *

# main function
def main():
    """ Play a game!
    """
    # declare variables
    g = Game()
    g.printState()
    player1 = g.players[0]
    player2 = g.players[1]
    # initialize win counts or score
    win_counts = [0, 0, 0]  # [p1 wins, p2 wins, ties]
    #calling functions when program is running
    exit = False
    while not exit:
        while not g.finished:
            g.nextMove()

        g.findFours()
        g.printState()

        if g.winner == None:
            win_counts[2] += 1

        elif g.winner == player1:
            win_counts[0] += 1

        elif g.winner == player2:
            win_counts[1] += 1
        # call print stats
        printStats(player1, player2, win_counts)
        # boolean statements that either loops through main again or terminates the program
        while True:
            play_again = str(input("Would you like to play again? "))
            # conditional statement to replay the game
            if play_again.lower() == 'y' or play_again.lower() == 'yes':
                g.newGame()
                g.printState()
                break
            # conditional statement that ends the game
            elif play_again.lower() == 'n' or play_again.lower() == 'no':
                print("Thanks for playing!")
                exit = True
                break
            else:
                print("I don't understand... "),

# outputs stats everytime a game is finished
def printStats(player1, player2, win_counts):
    print("{0}: {1} wins, {2}: {3} wins, {4} ties".format(player1.name,
                                                          win_counts[0], player2.name, win_counts[1], win_counts[2]))



if __name__ == "__main__":  # Default "main method" idiom.
    main()
    
```

## Results
The following analysis is based on a difficult levels of varying difficulties run for five games. The difficulty tested will
be in combinations of 1 and 1, 2 and 2, 3 and 3, 4 and 4, 1 and 2, 2 and 1, 2 and 3, 3 and 2, 3 and 4, 4 and 4. 10 games will be
played for each combination of difficulty levels. There will also be separate tests for the random function being applied and tests with only minimax and alpha
beta being applied.

### 1 and 1
Random Minimax: Bot1: 7 wins, Bot2: 3 wins, 0 ties
Minimax w/ Alpha Beta: Bot1: 10 wins, Bot2: 0 wins, 0 ties

Round: 38
        |   |   | o | o | x | x | x |
        |   |   | o | x | o | o | x |
        | X |   | o | o | o | x | o |
        | X | o | x | x | o | o | o |
        | X | x | x | o | x | x | o |
        | X | o | o | o | x | x | x |
          _   _   _   _   _   _   _ 
          1   2   3   4   5   6   7 

### 2 and 2
Random Minimax: Bot1: 5 wins, Bot2: 5 wins, 0 ties
Minimax w/ Alpha Beta: Bot1: 0 wins, Bot2: 10 wins, 0 ties

Round: 41
        | o |   | o | o | o | x | o |
        | x |   | x | x | o | x | x |
        | O | O | O | O | x | o | o |
        | x | x | x | o | o | o | x |
        | x | o | o | x | x | x | o |
        | o | x | x | x | o | x | x |
          _   _   _   _   _   _   _ 
          1   2   3   4   5   6   7 

### 3 and 3
Random Minimax: Bot1: 4 wins, Bot2: 6 wins, 0 ties
Minimax w/ Alpha Beta: Bot1: 0 wins, Bot2: 10 wins, 0 ties

Round: 19
        |   |   |   |   |   | O | x |
        |   |   |   |   |   | O | x |
        |   |   |   |   | o | O | o |
        |   |   |   |   | x | O | o |
        |   |   |   | x | x | x | o |
        |   |   |   | o | x | x | x |
          _   _   _   _   _   _   _ 
          1   2   3   4   5   6   7 

### 4 and 4
Random Minimax: Bot1: 5 wins, Bot2: 5 wins, 0 ties
Minimax w/ Alpha Beta: Bot1: 0 wins, Bot2: 10 wins, 0 ties

Round: 27
        |   |   |   |   | o | x | o |
        |   |   |   |   | x | o | x |
        |   |   | O |   | x | o | x |
        |   |   | O | x | o | o | x |
        |   |   | O | x | x | x | o |
        |   | x | O | o | o | x | x |
          _   _   _   _   _   _   _ 
          1   2   3   4   5   6   7 

### 1 and 2
Random Minimax: Bot1: 8 wins, Bot2: 2 wins, 0 ties
Minimax w/ Alpha Beta: Bot1: 10 wins, Bot2: 0 wins, 0 ties

Round: 24
        |   |   |   |   | o | o | x |
        |   |   |   |   | o | x | o |
        |   |   |   |   | x | x | o |
        |   |   |   | o | o | o | x |
        |   |   | X | X | X | X | o |
        |   |   | o | x | o | x | x |
          _   _   _   _   _   _   _ 
          1   2   3   4   5   6   7

### 2 and 1
Random Minimax: Bot1: 7 wins, Bot2: 3 wins, 0 ties
Minimax w/ Alpha Beta: Bot1: 0 wins, Bot2: 0 wins, 10 ties

Round: 43
        | o | o | x | o | x | o | o |
        | x | x | o | x | o | x | x |
        | x | x | o | x | x | o | x |
        | o | o | x | o | o | o | x |
        | x | o | o | o | x | x | o |
        | o | x | x | x | o | o | x |
          _   _   _   _   _   _   _ 
          1   2   3   4   5   6   7 

### 2 and 3
Random Minimax: Bot1: 4 wins, Bot2: 6 wins, 0 ties
Minimax w/ Alpha Beta: Bot1: 0 wins, Bot2: 10 wins, 0 ties

Round: 29
        |   |   |   |   | x | O | o |
        |   |   |   |   | O | x | x |
        |   |   | o | O | o | x | x |
        |   |   | O | x | x | o | x |
        |   | x | x | o | o | x | o |
        |   | x | o | x | o | o | x |
          _   _   _   _   _   _   _ 
          1   2   3   4   5   6   7 



### 3 and 2
Random Minimax: Bot1: 5 wins, Bot2: 5 wins, 0 ties
Minimax w/ Alpha Beta: Bot1: 0 wins, Bot2: 10 wins, 0 ties

Round: 43
        | O | x | o | o | x | o | o |
        | x | O | x | x | o | x | x |
        | o | x | O | o | x | x | o |
        | x | o | x | O | o | o | x |
        | o | x | o | o | x | x | o |
        | o | x | x | x | o | x | x |
          _   _   _   _   _   _   _ 
          1   2   3   4   5   6   7 

### 3 and 4
Random Minimax: Bot1: 7 wins, Bot2: 3 wins, 0 ties
Minimax w/ Alpha Beta: Bot1: 10 wins, Bot2: 0 wins, 0 ties

Round: 28
        |   |   |   |   | x | o | o |
        |   |   |   |   | o | x | o |
        |   |   | x | X | x | o | x |
        |   |   | o | o | X | o | x |
        |   |   | o | x | x | X | o |
        |   | x | o | o | o | x | X |
          _   _   _   _   _   _   _ 
          1   2   3   4   5   6   7 

### 4 and 3
Random Minimax: Bot1: 6 wins, Bot2: 4 wins, 0 ties
Minimax w/ Alpha Beta: Bot1: 0 wins, Bot2: 0 wins, 10 ties

Round: 43
        | o | o | o | x | x | o | x |
        | x | x | x | o | o | x | x |
        | x | o | o | x | x | o | x |
        | o | x | x | o | o | x | o |
        | o | x | o | x | o | o | o |
        | o | o | x | o | x | x | x |
          _   _   _   _   _   _   _ 
          1   2   3   4   5   6   7 

## Analysis
Through random minimax testing, I expected that a difficulty of equal values would generate an even amount of wins for each bot. 
This occurred between a range of 3 to 7 wins for either bot. I also expected an unequal difficulty to favor the bot with the lower difficulty.
This was not the case when testing '2 and 1', '2 and 3', '3 and 2', '4 and 3'. The offset of difficulty in these tests seemed to mimic random minimax results.

When testing with alpha beta algorithm where difficulty is equal, bot2 was unanimously the winner except for when the difficulty was '1 and 1' in which bot 1 was the unanimous winner.
This could simply be due to the winner being the bot that played first. With unequal difficulty levels, I would again expect the bot with the lower difficulty to win. This was not the 
case with '2 and 3' where bot 2 was the unanimous winner. In '2 and 1', '4 and 3' the offset in difficulty resulted in a tie which leads me to conclude the alpha beta algorithm can be neutralized with a slight offset of difficulty.

## Works Cited

1. Francis. (2021, February 10). Connect 4 with Minimax algorithm. Madjakul. Retrieved November 8, 2022, from https://www.madjakul.com/en/posts/minimax_connect4/#to-conclude 
2. Ackermann, E. (2015, November 5). Connect-four/minimax.py at master · Erikackermann/connect-four. GitHub. Retrieved November 8, 2022, from https://github.com/erikackermann/Connect-Four/blob/master/minimax.py 
