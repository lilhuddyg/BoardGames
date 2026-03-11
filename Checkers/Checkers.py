class Checkers:
    def __init__(self):
        self.board = self.createBoard()
        self.nextToPlay = "W"
        self.numPieces = {"W":12, "B":12}
    
    def play(self):
        while self.numPieces["W"] > 0 and self.numPieces["B"] > 0:
            printBoard(self.board)

            while True: # Select a piece
                i, j = map(int, input(f"Which {self.nextToPlay} piece do you want to move (row col)?: ").split())

                if not (inbounds(i) and inbounds(j)): # If the move is out of bounds
                    print("Invalid Move. Coordinates out of bounds.")
                elif self.board[i][j] != self.nextToPlay: # Wrong piece or blank square
                    print("That square is not your piece!")
                elif len(self.getValidMoves(i, j, self.nextToPlay)) == 0:
                    print("That piece has no valid moves!")
                else: # In bounds and right color
                    break
            
            movedAlready = False
            capturedAlready = False
            # Do valid moves while the piece can still jump
            while (not movedAlready and len(self.getValidMoves(i, j, self.nextToPlay)) > 0) or (capturedAlready and len(self.getValidJumps(i, j, self.nextToPlay)) > 0):
                validMoves = self.getValidMoves(i, j, self.nextToPlay) if not capturedAlready else self.getValidJumps(i, j, self.nextToPlay)
                displayBoard = [row.copy() for row in self.board]
                print(f"Valid Moves: {[move[0] for move in validMoves]}")
                for move in validMoves:
                    displayBoard[move[0][0]][move[0][1]] = "*"
                printBoard(displayBoard)
                
                while True:
                    di, dj = map(int, input(f"Where do you want to move the {self.nextToPlay} piece at {i} {j}?: ").split())

                    if not (inbounds(di) and inbounds(dj)) or displayBoard[di][dj] != "*" : # Move is OOB or not valid
                        print("Invalid Move. Choose one of the valid moves.")
                    else: # Inbounds and valid move
                        break

                # Get the move
                chosenMove = None
                for move in validMoves:
                    if (di,dj) == move[0]: # This is the move
                        chosenMove = move
                        isCapture = chosenMove[1]
                        ci, cj = chosenMove[2]
                
                self.board[i][j] = "."
                self.board[di][dj] = self.nextToPlay
                if isCapture:
                    self.numPieces[self.board[ci][cj]] -= 1
                    self.board[ci][cj] = "."
                    capturedAlready = True

                i, j = di, dj # For double jumping purposes
                movedAlready = True
            
            self.nextToPlay = "W" if self.nextToPlay == "B" else "B"
        
        winner = "W" if self.numPieces["B"] <= 0 else "B"
        print(f"{winner} wins!")
            
    def getValidMoves(self, i, j, symbol):
        deltas = [[-1, -1], [-1, 1]]
        toReturn = []

        for delta in deltas:
            delta = [delta[0]*-1, delta[1]*-1] if symbol == "B" else delta  # Sets direction based on color
            newI, newJ = i+delta[0], j+delta[1]
            
            if inbounds(newI) and inbounds(newJ): # Both are inbounds
                if self.board[newI][newJ] == symbol: # Can't capture your piece
                    continue
                elif self.board[newI][newJ] == ".": # Empty, Valid Move
                    toReturn.append([(newI, newJ), False, (-1, -1)])
                else: # There's an enemy piece in the way
                    enemyPiece = self.board[newI][newJ]
                    landI, landJ = newI+delta[0], newJ+delta[1]
                    if inbounds(landI) and inbounds(landJ) and self.board[landI][landJ] == ".": # If we can jump to an empty spot
                        toReturn.append([(landI, landJ), True, (newI, newJ)])

        return toReturn

    def getValidJumps(self, i, j, symbol):
        validMoves = self.getValidMoves(i, j, symbol)
        return [move for move in validMoves if move[1] == True] # Returns only the valid jumps

    def createBoard(self):
        def right(symbol):
            return [".", symbol]*4
        def left(symbol):
            return [symbol, "."]*4
        
        toReturn = []
        for row in range(8):
            if row in [3, 4]:
                toReturn.append(["."]*8)
            elif row in [1, 5, 7]:
                toReturn.append(left("W" if row > 4 else "B"))
            elif row in [0, 2, 6]:
                toReturn.append(right("W" if row > 4 else "B"))
        
        return toReturn

def printBoard(board):
    print("    ", end="")
    print("    ".join([str(i) for i in range(8)]))
    for idx,row in enumerate(board):
        print(f"{idx} {row}")

def inbounds(coord):
    return 0 <= coord < 8

print("Welcome to Checkers.")
game = Checkers()
game.play()