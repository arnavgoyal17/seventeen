"""
Version 2. Batch Mode

After you have Version 1 working, you can proceed to implement Version 2, which plays the Seventeen Game in batch mode.
The program reads from an input file (named 'i206_placein_input.txt') a sequence of comma delimited numbers 
representing the sequence of moves made by Player 1. Each line of the input file represents a different game. 
For example, the sample input file contains data for ten games. In the first game, 
Player 1 removes 3 marbles during its first turn, 1 marble during its second turn, three marbles during its third turn, and so on.

If the number of marbles left in the jar is fewer than the next number in the play sequence, 
then Player 1 should remove all the remaining marbles. For example, if there are two marbles left in the jar, 
and the next number in the sequence is 3, then Player 1 should remove two marbles, not three.
Player 2 will play the same marble-removal strategy as in Version 1.

Note that not all numbers in each line may be used, depending on the progress of the game 
(which in turn depends on the strategy used by Player 2). 
Conversely, the play sequences are generated such that there will always be enough numbers for each game.

The program will play the game as many times as there are lines in the input file, 
printing the sequence of moves and the game winner into an output text file 
(named i206_placein_output2_<ischool_userid>.txt'), one line per game. 
At the end of all the games, the program will print the number of games won by each player

"""

# Imports
import random
import itertools

# Body

# define global variables
nMarbles = 17
# listValidInput = [1,2,3]
gameMoves = [] # will store a list of two elements, who played the last turn and how many marbles were removed
continueGame = True # if false, the game will end and announce the winner
numberGame = 0 # Counter for the number of games that are being played
p1Wins = 0 # Counter to note the number of games Player 1 wins
p2Wins = 0 # Counter to note the number of games Player 2 wins
outputFile = open("i206_placein_output2_arnavgoyal.txt", "w")

def GetUserInput(userInput):
    """
    This function takes the input from the user and validates the input.
    1. Input should be either 1,2,3 and at the same time not more than the number of marbles left in the jar
    2. Prompts the user again and again till a valid input is entered
    """
    
    userIntInput = int(userInput)

    # check if the input can be used or not. If not, return the number of marbles in the jar
    if(userIntInput > nMarbles):
        return nMarbles
    else:
        return userIntInput

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

def DetermineWinner(listMoveSequences):
    """
    This function checks the moves to know who played the last move. Prints the winner
    """

    global p1Wins
    global p2Wins

    lastPlayer = int(gameMoves[0][0])
    playSeq = "-".join(listMoveSequences)
    if(lastPlayer == 0):
        winner = "P2"
        p2Wins += 1
        outputFile.write("Game #{}. Play sequence: {}. Winner: {}\n".format(numberGame, playSeq, winner))
    else:
        winner = "P1"
        p1Wins += 1
        outputFile.write("Game #{}. Play sequence: {}. Winner: {}\n".format(numberGame, playSeq, winner))

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
            maxMarbles = min(maxMarbles, nMarbles)
            removeMarbles = random.randint(1, maxMarbles)
            RemoveMarbles(removeMarbles)
            marblesRemoved = removeMarbles
    else:
        maxMarbles = min(maxMarbles, nMarbles)
        removeMarbles = random.randint(1, maxMarbles)
        RemoveMarbles(removeMarbles)
        marblesRemoved = removeMarbles

    # print("\nComputer's turn...")
    # print("Computer removed {} marbles.".format(marblesRemoved))
    return marblesRemoved

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

def StartGame(listUserInput):
    """
    The main function that runs the game
    """
    whoseTurn = 0 # defaults to 0 to define that the Human plays the 1st turn
    moveSequences = []

    while continueGame:
        if(whoseTurn == 0):
            # Player 1's Turn. Get the 1st number from the list and check if its valid or not
            userInput = GetUserInput(listUserInput.pop(0))
            RemoveMarbles(userInput)
            moveSequences.append(str(userInput))

            # add the last move to the list
            AddMoves(whoseTurn, userInput)

            # change whoseTurn so that the Computer could play the next turn
            whoseTurn = (whoseTurn + 1) % 2
        else:
            # Computer's turn. Call the function
            userLastMove = GetLastUserInput()
            computerTurn = ComputerTurn(userLastMove)
            moveSequences.append(str(computerTurn))
            # change whoseTurn so that the Human could play the next turn
            
            AddMoves(whoseTurn, computerTurn)
            whoseTurn = (whoseTurn + 1) % 2

        CanPlayMore()

    # You only break out of the loop when the game finishes
    DetermineWinner(moveSequences)

def PlayGame():
    """
    This function would read the .txt file line by line and call StartGame() by passing the player moves in a list
    """
    global numberGame
    global nMarbles
    global gameMoves
    global continueGame
    moveSeq = ''
    gameWinner = ''

    # open the file and loop through every line
    with open("i206_placein_input.txt", "r") as inputFile:
        for lines in inputFile:
            listUserInput = lines.strip().split(",")

            # pass the input to the StartGame() function which would play the game and return the winner and the sequence of moves
            numberGame = numberGame + 1
            nMarbles = 17
            gameMoves.clear()
            continueGame = True
            StartGame(listUserInput)

    outputFile.write("Player 1 won {} times; Player 2 won {} times.\n".format(p1Wins, p2Wins))
    outputFile.close()


def main():
    # print("Let's play the game of Seventeen!")
    # PrintMarbles()
    PlayGame()

if __name__ == '__main__':
    main()
