"""

The Seventeen Game

"Seventeen" is a simple mathematical strategy game, where two players take turns removing marbles from a jar, 
and the player who removes the last marble loses the game.

The jar begins with seventeen marbles, and each player can remove one, two, or three marbles during each turn.

Version 1. Interactive Mode

The program should allow a human to play against a computer. The human always goes first. If the human enters incorrect input
(anything other than 1, 2, 3, or a number larger than the number of marbles remaining in the jar), 
an error message should be displayed, and the human is prompted to try again.

The computer player can choose to remove marbles according to any strategy of your choosing. 
Some examples include: (i) always choose the same number as the human player, (ii) choose randomly. 
Note that it is possible, though not required for this exam, 
to devise a straightforward strategy for the computer such that it will never lose, as long as the human player goes first.

At the end of each turn, the program should print out the number of marbles removed in the previous turn, 
and the number of marbles that remain in the jar. Once there are no more marbles in the jar, 
the program should declare the winner of the game.

"""

# Imports
import random
import itertools

# Body

# define global variables
nMarbles = 17
listValidInput = [1,2,3]
gameMoves = [] # will store a list of two elements, who played the last turn and how many marbles were removed
continueGame = True # if false, the game will end and announce the winner

def GetUserInput():
    """
    This function takes the input from the user and validates the input.
    1. Input should be either 1,2,3 and at the same time not more than the number of marbles left in the jar
    2. Prompts the user again and again till a valid input is entered
    """
    
    # try block that attempts to convert the input into an integer
    try:
        userInput = int(input("\nYour turn: How many marbles will you remove (1-3)? "))
        if(userInput in listValidInput and userInput <= nMarbles):
            return userInput
        else:
            raise ValueError
    except ValueError:
        print("Sorry, that is not a valid option. Try again!")        
        PrintMarbles()

        # call the function again to get UserInput
        return GetUserInput()

def PrintMarbles():
    """
    Print the number of remaining marbles in the jar
    """
    print("Number of marbles left in jar: {}".format(nMarbles))

def RemoveMarbles(n):
    """
    This function removes 'n' marbles from the Jar. The input is pre-validated and 
    hence the number of marbles will never go below 0
    """
    global nMarbles
    nMarbles = nMarbles - n

def CanPlayMore():
    """
    This function will determine if the game can be played more. If yes, it would change the keep continueGame = True
    Else, it will make continueGame = false
    """
    global continueGame

    # check if there are marbles left
    if(nMarbles > 0):
        continueGame = True
    else:
        continueGame = False

def DetermineWinner():
    """
    This function checks the moves to know who played the last move. Prints the winner
    """

    lastPlayer = int(gameMoves[0][0])
    if(lastPlayer == 0):
        print("\nThere are no marbles left. Computer wins!")
    else:
        print("\nThere are no marbles left. Human wins!")


def ComputerTurn(n):
    """
    Call the function whenever the computer is required to remove marbles. The last input given by the user is given as the input

    The computer can use two different strategies
    1. Remove the same number of Marbles as the user (If that's allowed)
        If not allowed then use strategy #2
    2. Remove a random number (1, 2, 3)
    """

    nStrat = random.randint(1,2)
    maxMarbles = 3 # define the maximum marbles you can remove. This might change if there are not enough marbles in the jar
    marblesRemoved = 0

    if(nStrat == 1):
        # check if you can remove the same marbles as the user
        if(n <= nMarbles):
            RemoveMarbles(n)
            marblesRemoved = n
        else:
            nStrat = 2
            maxMarbles = min(maxMarbles, nMarbles)
            removeMarbles = random.randint(1, maxMarbles)
            RemoveMarbles(removeMarbles)
            marblesRemoved = removeMarbles
    else:
        maxMarbles = min(maxMarbles, nMarbles)
        removeMarbles = random.randint(1, maxMarbles)
        RemoveMarbles(removeMarbles)
        marblesRemoved = removeMarbles

    print("\nComputer's turn...")
    print("Computer removed {} marbles.".format(marblesRemoved))

    # add the last move to the gameMoves list
    AddMoves(1, marblesRemoved)

def AddMoves(player, number):
    """
    This function adds the players move to the list of moves. Always adds to the 1st position
    """
    gameMoves.insert(0, [player, number])

def GetLastUserInput():
    """
    Return the number of marbles the user removed in the last move
    """
    return int(gameMoves[0][1])


def StartGame():
    """
    The main function that runs the game
    """
    whoseTurn = 0 # defaults to 0 to define that the Human plays the 1st turn

    while continueGame:
        if(whoseTurn == 0):
            # Human's turn. Prompt for user input
            userInput = GetUserInput()
            RemoveMarbles(userInput)
            print("You removed {} marbles.".format(userInput))
            PrintMarbles()

            # add the last move to the list
            AddMoves(whoseTurn, userInput)

            # change whoseTurn so that the Computer could play the next turn
            whoseTurn = (whoseTurn + 1) % 2
        else:
            # Computer's turn. Call the function
            userLastMove = GetLastUserInput()
            ComputerTurn(userLastMove)
            PrintMarbles()

            # change whoseTurn so that the Human could play the next turn
            whoseTurn = (whoseTurn + 1) % 2

        CanPlayMore()

    # You only break out of the loop when the game finishes
    DetermineWinner()

def main():
    print("Let's play the game of Seventeen!")
    PrintMarbles()
    StartGame()

if __name__ == '__main__':
    main()
