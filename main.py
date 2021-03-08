from tkinter import *
from tkinter import messagebox
import random


class Game():
    def __init__(self):
        self.window = Tk()
        self.window.title("15 Game")
        # self.window.rowconfigure(0, weight=1)
        # self.window.columnconfigure(0, weight=1)

        self.frame = Frame(self.window)
        self.frame.grid(column=0, row=0, sticky="NEWS")
        self.btnNew = Button(self.frame, text="New", command=self.new_game)
        self.btnNew.grid(row=0, column=0, columnspan=2, sticky="")
        self.btnExit = Button(self.frame, text="Exit", command=self.window.destroy)
        self.btnExit.grid(row=0, column=2, columnspan=2, sticky="")

        self.new_game()

    def draw_buttons(self):
        for i in range(1, 5):
            for j in range(0, 4):
                self.frame.rowconfigure(i, weight=1)
                self.frame.columnconfigure(j, weight=1)

                pos = 4 * (i - 1) + j
                if self.numbers[pos] == "":
                    self.btnGame = Button(self.frame, text="")
                    self.btnGame.grid(row=i, column=j)
                else:
                    self.btnGame = Button(self.frame, text=str(self.numbers[pos]))
                    self.btnGame.bind("<Button-1>", self._change_state(self.numbers, i - 1, j))
                    self.btnGame.grid(row=i, column=j, sticky="WE")

        self.frame.pack()
        self.check_win()

    def change_state(self, numbers, x, y):
        pos = 4 * x + y
        if x > 0 and self.numbers[pos - 4] == "":
            self.swap(pos - 4, pos)
        elif x < 3 and self.numbers[pos + 4] == "":
            self.swap(pos + 4, pos)
        elif y > 0 and self.numbers[pos - 1] == "":
            self.swap(pos - 1, pos)
        elif y < 3 and self.numbers[pos + 1] == "":
            self.swap(pos + 1, pos)

        self.draw_buttons()

    def swap(self, emptyInd, pos):
        self.numbers[emptyInd] = self.numbers[pos]
        self.numbers[pos] = ""

    def _change_state(self, numbers, x, y):
        def change_state_(event):
            self.change_state(numbers, x, y)

        return change_state_

    def check_win(self):
        if self.numbers[0] == "":
            for i in range(1, 16):
                if self.numbers[i] != i:
                    return
        else:
            for i in range(15):
                if self.numbers[i] != i + 1:
                    return

        messagebox.showinfo(message="You win!")
        self.new_game()

    def new_game(self):
        self.numbers = [x for x in range (1,16)]
        self.numbers.append("")
        random.shuffle(self.numbers)

        self.draw_buttons()

    def start_game(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = Game()
    game.start_game()
