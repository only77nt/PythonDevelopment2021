import tkinter as tk
from tkinter import font


class InputLabel(tk.Label):
    def __init__(self, master=None):
        self.label_font = font.Font(family='Monospace', size=24, weight='normal')
        tk.Label.__init__(self, master,
                          text_="",
                          takefocus_=True,
                          highlightthickness_=2,
                          highlightcolor_='green',
                          borderwidth_=4,
                          font_=self.label_font,
                          justify_='right',
                          anchor_='w',
                          relief=tk.GROOVE)

        self.bind('<Any-Key>', self.on_key_pressed)
        self.bind('<Button-1>', self.on_mouse_click)
        self.bind('<FocusIn>', self.activate_cursor)
        self.bind('<FocusOut>', self.deactivate_cursor)

        self.cursor_create()

    def cursor_create(self):
        self.cursor_pos = 0
        self.frame = tk.Frame(self, borderwidth=5, background="red", height=30, width=2)
        self.cursor_place()

    def cursor_place(self):
        x = self.label_font.measure(self['text'][:self.cursor_pos])
        h = self.label_font.metrics('linespace')
        self.frame.place(x=x, y=self.winfo_height() // 10, width=1, height=h)

    def on_mouse_click(self, event):
        self.focus_set()
        if len(self['text']) > 0:
            char_width = self.label_font.measure(self['text']) // len(self['text'])
        else:
            char_width = self.label_font.measure(' ')
        self.cursor_pos = min(event.x // char_width, len(self['text']))
        self.cursor_place()

    def on_key_pressed(self, event):
        if event.keysym == 'Left':
            self.cursor_pos = max(0, self.cursor_pos - 1)
        elif event.keysym == 'Right':
            self.cursor_pos = min(self.cursor_pos + 1, len(self['text']))
        elif event.keysym == 'Home':
            self.cursor_pos = 0
        elif event.keysym == 'End':
            self.cursor_pos = len(self["text"])
        elif event.keysym == 'Delete':
            if self.cursor_pos > 0:
                self.configure(text=self['text'][:self.cursor_pos] + self['text'][self.cursor_pos + 1:])
        elif event.keysym == 'BackSpace':
            if self.cursor_pos <= len(self['text']):
                self["text"] = self["text"][:self.cursor_pos - 1] + self["text"][self.cursor_pos:]
                self.cursor_pos -= 1
        elif event.char and event.char.isprintable():
            self["text"] = self["text"][:self.cursor_pos] + event.char + self["text"][self.cursor_pos:]
            self.cursor_pos += 1

        self.cursor_place()

    def activate_cursor(self, event):
        self.frame.configure(background='green')

    def deactivate_cursor(self, event):
        self.frame.configure(background='red')


class Application(tk.Frame):
    def __init__(self, master=None):
        self.root = tk.Tk()
        self.root.title("InputLabel")

        tk.Frame.__init__(self, master)
        self.grid()
        self.lable = InputLabel(self)
        self.lable.grid(row=1, column=0, sticky='NEWS')
        self.quit_button = tk.Button(self, text='Quit', command=self.quit)
        self.quit_button.grid(row=2, column=0, sticky='E')
        self.columnconfigure(0, weight=1)

    def start(self):
        self.mainloop()


def main():
    app = Application()
    app.start()


if __name__ == '__main__':
    main()
