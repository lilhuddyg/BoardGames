# Code for an M x N Tic-Tac-Toe Game
class TicTacToe:
    def __init__(self, m, n, numToWin):
        self.m = m
        self.n = n
        self.numToWin = numToWin
        self.board = [["."]*n for _ in range(m)]
        self.nextToPlay = "X"
        self.numMovesPlayed = 0
    
    def play(self):
        self.printBoard()

        while True:
            while True:
                i, j = map(int, input(f"Enter move for {self.nextToPlay} (row col): ").split())

                if not (0 <= i < self.m and 0 <= j < self.n): # If out of bounds
                    print("Invalid Move. Out of bounds")
                elif self.board[i][j] != ".":
                    print(f"Invalid Move. Square already taken. {i}, {j} has {self.board[i][j]}")
                else:
                    break

            self.board[i][j] = self.nextToPlay
            self.printBoard()
            
            win = self.checkWin(i,j)
            if win:
                print(f"{self.nextToPlay} won!")
                break

            self.numMovesPlayed += 1
            if self.numMovesPlayed == self.m * self.n: # Board filled up
                print("Draw!")
                break

            self.nextToPlay = "X" if self.nextToPlay == "O" else "O"
            print()

    # Checks for a win on an m x n board
    def checkWin(self, i, j):
        symbol = self.board[i][j]
        deltas = [[[1,0],[-1,0]],
                  [[0,1],[0,-1]],
                  [[1,1],[-1,-1]],
                  [[1,-1],[-1,1]]]
        
        for fwdDir, backDir in deltas:
            fwdCt = 0; backCt = 0
            newI, newJ = i, j
            # Iter Forward
            while 0 <= newI < len(self.board) and 0 <= newJ < len(self.board[0]) and self.board[newI][newJ] == symbol:
                fwdCt += 1
                newI += fwdDir[0]
                newJ += fwdDir[1]
                #print(fwdCt)
            
            newI, newJ = i, j
            # Iter Backward
            while 0 <= newI < len(self.board) and 0 <= newJ < len(self.board[0]) and self.board[newI][newJ] == symbol:
                backCt += 1
                newI += backDir[0]
                newJ += backDir[1]
                #print(backCt)
            
            totalCt = fwdCt + backCt - 1
            #print(totalCt)
            if totalCt >= self.numToWin:
                return True
        
        return False
    
    def printBoard(self):
        print("    ", end="")
        print("    ".join([str(i) for i in range(self.n)]))
        for idx,row in enumerate(self.board):
            print(f"{idx} {row}")
        #print()

print("Welcome to Tic Tac Toe. ")
game = TicTacToe(3,3,3)
game.play()