import tkinter as tk
from tkinter import ttk
import re


class Application(tk.Frame):
    def __init__(self, master=None):
        self.root = tk.Tk()
        self.root.title("Graphics editor")

        tk.Frame.__init__(self, master)

        self.c = tk.Canvas(self, bg='white')
        self.c.bind('<ButtonPress-1>', self.on_mouse_click)
        self.c.bind('<ButtonRelease-1>', self.on_mouse_release)
        self.c.grid(row=0, column=0, rowspan=2, columnspan=6, sticky='NEWS')
        self.rowconfigure(0, weight=1)

        self.t = tk.Text(self)
        self.t.grid(row=0, column=6, rowspan=2, columnspan=2)
        self.t.tag_config("wrong", background="red")

        self.l1 = tk.Label(self, text="Цвет заливки: ", font='Arial')
        self.l1.grid(row=2, column=0)
        self.color_choice = ttk.Combobox(self,
                                         values=[
                                             'green',
                                             'red',
                                             'yellow',
                                             'black',
                                             'blue'])
        self.color_choice.current(2)
        self.color_choice.grid(row=2, column=1)

        self.l2 = tk.Label(self, text="Цвет границы: ", font='Arial')
        self.l2.grid(row=2, column=2)
        self.border_color_choice = ttk.Combobox(self,
                                                values=[
                                                    'green',
                                                    'red',
                                                    'yellow',
                                                    'black',
                                                    'blue'])
        self.border_color_choice.current(1)
        self.border_color_choice.grid(row=2, column=3)

        self.l3 = tk.Label(self, text="Размер границы: ", font='Arial')
        self.l3.grid(row=2, column=4)
        spinbox_default = tk.StringVar(self)
        spinbox_default.set("5")
        self.border_width = tk.Spinbox(self, from_=0, to=50, textvariable=spinbox_default)
        self.border_width.grid(row=2, column=5)

        self.cb = tk.Button(self, text="Стереть всё", command=self.delete_all, font='Arial')
        self.cb.grid(row=2, column=6)

        self.tb = tk.Button(self, text="Обновить картинку по тексту", command=self.change_picture, font='Arial')
        self.tb.grid(row=2, column=7)

        self.grid()

    def on_mouse_click(self, event):
        item = self.c.find_withtag(tk.CURRENT)
        self.mouse_press = event.x, event.y
        if item:
            self.exist_flag = True
            self.item = item
        else:
            self.exist_flag = False
            self.item = None

    def on_mouse_release(self, event):
        if self.exist_flag:
            self.c.move(self.item, event.x - self.mouse_press[0], event.y - self.mouse_press[1])
        else:
            self.c.create_oval(self.mouse_press[0], self.mouse_press[1], event.x, event.y,
                               width=self.border_width.get(), outline=self.border_color_choice.get(),
                               fill=self.color_choice.get())
        self.change_text()

    def change_text(self):
        self.t.delete('1.0', tk.END)
        for item in self.c.find_all():
            s = "oval: coords - " + str(", ".join(map(str, self.c.coords(item)))) + ", border_width - " + str(
                self.c.itemcget(item, 'width')) + ", border_color - " + str(
                self.c.itemcget(item, 'outline')) + ", fill_color - " + str(self.c.itemcget(item, 'fill')) + "!\n"
            self.t.insert(tk.END, s)

    def change_picture(self):
        s = self.t.get("1.0", tk.END).splitlines()
        self.t.tag_delete("wrong")
        self.c.delete("all")
        for i in range(len(s)):
            if s[i]:
                result = re.sub(
                    "oval: coords - (.*), (.*), (.*), (.*), border_width - (.*), border_color - (.*), fill_color - (.*)!",
                    "", s[i])

                if result == "":
                    pattern = re.findall(
                        "oval: coords - (.*), (.*), (.*), (.*), border_width - (.*), border_color - (.*), fill_color - (.*)!",
                        s[i])

                    coords = pattern[0][:4]
                    width = pattern[0][4]
                    color = pattern[0][5]
                    fill_color = pattern[0][6]
                    self.c.create_oval(*coords, width=width, outline=color, fill=fill_color)
                else:
                    self.t.tag_add("wrong", f"{i + 1}.0", f"{i + 1}.end")
        self.t.tag_config("wrong", background="red")

    def delete_all(self):
        self.c.delete("all")
        self.t.delete('1.0', tk.END)

    def start(self):
        self.mainloop()


def main():
    app = Application()
    app.start()


if __name__ == '__main__':
    main()
