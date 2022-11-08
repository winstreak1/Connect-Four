# Python Final Project
# Connect Four
#
# Erik Ackermann
# Charlene Wang
#
# Play connect four
# February 27, 2012
# Accessed and revised by Peter Mavronicolas Nov. 8,2022

from connect4 import *

# mqin function
def main():
    """ Play a game!
    """
    # declare variables
    g = Game()
    g.printState()
    player1 = g.players[0]
    player2 = g.players[1]

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

        printStats(player1, player2, win_counts)
        # statement that either loops through main again or terminates the program
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