import tkinter as tk
from random import randint
from copy import deepcopy

class TopLayer:
    def __init__(self, root, tx):
        self.text = tk.StringVar()
        self.text.set(tx)
        self.label = tk.Label(root, textvariable=self.text)
        self.label.configure(bg='black', fg="white", width=200)
        self.label.pack()

class GameCanvas:
    def __init__(self, root, pos):
        global game

        self.root = root
        
        self.id = pos
        self.x = (pos % 3) * 210
        self.y = (pos // 3) * 210 + 20
        self.canvas = tk.Canvas(root, width=200, height=200, bg='#ffffff',
                                borderwidth=0, highlightthickness=0)
        self.canvas.place(x=self.x, y=self.y)
        self.canvas.bind("<Button-1>", self.onclick)

        self.value = 2

    def onclick(self, event):
        
        game.newTurn(self.id)

    def draw(self, turn):
        if(game.turn == 0):
            self.canvas.create_line(10, 10, 190, 190, width=10, fill="#000000")
            self.canvas.create_line(10, 190, 190, 10, width=10, fill="#000000")
            self.value = 0
        else:
            self.canvas.create_oval(10, 10, 190, 190, fill="#000000")
            self.canvas.create_oval(20, 20, 180, 180, fill="#ffffff")
            self.value = 1

class Bot1:
    
    def play(self, b, legalMoves):


        best = 10000
        bestCase = -1

        for i in legalMoves:
            board = deepcopy(b)
            board[i] = 1
            updatedLegalMoves = deepcopy(legalMoves)
            updatedLegalMoves.remove(i)
            val = self.minimax(board, updatedLegalMoves, 0, 0)
            print(val)
            if(val < best):
                bestCase = i
                best = val
        print('----------')
        return bestCase


    def minimax(self, b, legalMoves, depth, player):

        score = 0
        nextPlayer = 1 if(player == 0) else 0
        (win, p) = self.checkWin(b)

        if(win == True and p == 1):
            score = -10 + depth
        elif(win == True and p == 0):
            score = 10 - depth
        if(score != 0 or len(legalMoves) == 0):
            return score

        if(player): # Minimizer
            score = 10000
            for i in legalMoves:
                board = deepcopy(b)
                board[i] = player
                updatedLegalMoves = deepcopy(legalMoves)
                updatedLegalMoves.remove(i)
                score = min(score, self.minimax(board, updatedLegalMoves, depth+1, nextPlayer))
            return score
        
        else: # Maximizer
            score = -10000
            for i in legalMoves:
                board = deepcopy(b)
                board[i] = player
                updatedLegalMoves = deepcopy(legalMoves)
                updatedLegalMoves.remove(i)
                score = max(score, self.minimax(board, updatedLegalMoves, depth+1, nextPlayer))
            return score

    
    def checkWin(self, board):
        #https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/

        for j in range(3):
            row = col = diag = antidiag = 0
            for i in range(3):

                if(board[3*i + j] == 0):
                    col += 1
                elif(board[3*i + j] == 1):
                    col -= 1

                if(board[3*j + i] == 0):
                    row += 1
                elif(board[3*i + j] == 1):
                    col -= 1

                if(board[0] == board[4] == board[8] == 0):
                    diag += 1
                elif(board[0] == board[4] == board[8] == 1):
                    diag -= 1

                if(board[2] == board[4] == board[6] == 0):
                    antidiag += 1
                elif(board[2] == board[4] == board[6] == 0):
                    antidiag -= 1

            if(row == 3 or col == 3 or diag == 3 or antidiag == 3):
                return (True, 0)
            if(row == -3 or col == -3 or diag == -3 or antidiag == -3):
                return (True, 1)

        return (False, 2)


class GameArea:
    def __init__(self, root):
        
        self.root = root
        
        self.mode = 0

        self.showMenu()

    def showMenu(self):
        self.text = tk.Label(self.root, text="Jeu de morpion", bg="white")
        self.text.configure(font=('TkDefaultFont', 40))
        self.text.place(x=110, y=100)
        self.btn1p = tk.Button(self.root, text="Joueur VS bot", command=self.startPvB, height=3, width=30)
        self.btn1p.place(x=180, y=350)
        self.btn2p = tk.Button(self.root, text="Joueur VS joueur", command=self.startPvP, height=3, width=30)
        self.btn2p.place(x=180, y=450)

    def startPvB(self):
        self.mode = 2
        self.bot = Bot1()
        self.startGame()

    def startPvP(self):
        self.mode = 1
        self.startGame()

    def startGame(self):

        for child in self.root.winfo_children():
            child.destroy()

        if(self.mode == 1):
            self.text = TopLayer(self.root, 'Au tour du joueur X')
        else:
            self.text = TopLayer(self.root, 'Joueur VS robot')

        self.btn1p = 0
        self.btn2p = 0

        self.root.configure(bg="black")
        self.counter = 0
        self.turn = 0
        self.canvGrid = []
        self.numGrid = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for i in range(9):
            self.canvGrid.append(GameCanvas(root, i))

    def stopGame(self):
        self.root.configure(bg="white")
        for child in self.root.winfo_children():
            child.destroy()
        
        txt = 'Les X ont gagné !' if self.turn == 0 else ('Les O ont gagné !' if self.turn == 1 else 'C\'est une égalité')
        self.text = tk.Label(self.root, text=txt, bg="white")
        self.text.configure(font=('TkDefaultFont', 40))
        self.text.place(x=90, y=100)
        self.btn1p = tk.Button(self.root, text="Rejouer", command=self.startGame, height=3, width=30)
        self.btn1p.place(x=180, y=350)
        self.btn2p = tk.Button(self.root, text="Quitter", command=self.quit, height=3, width=30)
        self.btn2p.place(x=180, y=450)

    def checkWin(self, x, y):
        row = col = diag = antidiag = 0
        for i in range(3):
            if(self.canvGrid[3*i + x].value == self.turn):
                row += 1
            if(self.canvGrid[3*y + i].value == self.turn):
                col += 1
            if(self.canvGrid[3*i + i].value == self.turn):
                diag += 1
            if(self.canvGrid[3*(2-i) + i].value == self.turn):
                antidiag += 1
        if(self.counter == 8 and not (row == 3 or col == 3 or diag == 3 or antidiag == 3 or self.counter == 8)):
            self.turn = 2
        if(row == 3 or col == 3 or diag == 3 or antidiag == 3 or self.counter == 8):
            return True
        return False
    
    def playBot(self):

        board = []
        for i in self.canvGrid:
            board.append(i.value)
        numGrid = deepcopy(self.numGrid)
        x = self.bot.play(board, numGrid)
        return x
        #x = randint(0, len(self.numGrid) - 1)
        #return self.numGrid[x]
    
    def newTurn(self, pos):
        if(pos in self.numGrid):
            self.canvGrid[pos].draw(self.turn)
        
            self.numGrid.remove(pos)

            if(self.checkWin(pos % 3, pos // 3)):
                self.stopGame()
                return
            
            if(self.turn == 0):
                self.turn = 1
                if(self.mode == 1):
                    self.text.text.set("Au tour du joueur O")
                else:
                    self.newTurn(self.playBot())
            else:
                self.turn = 0
                if(self.mode == 1):
                    self.text.text.set("Au tour du joueur X")
            self.counter += 1
    
    def quit(self):
        self.root.destroy()
            
        


root = tk.Tk()
root.title("Futur morpion")
root.geometry("620x640")
root.resizable(0,0)
root.configure(bg="white")

game = GameArea(root)

root.mainloop()

