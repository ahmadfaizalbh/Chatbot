from os import path
from tkinter import Tk, Canvas, Frame, Label, \
    ALL, Button, Entry, END, Scrollbar, N, S, E, W, LEFT, PhotoImage
from tkinter.constants import DISABLED, NORMAL, RIGHT
from threading import Thread, Event
from time import sleep


class ChatGUI:
    def __init__(self, callback, first_message="welcome to ChatBotAI", terminate="quit"):
        self.data_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), "media")
        self.last_bubble = None
        self.thread_event = Event()
        self.callback = callback
        self.terminate = terminate
        self.root = Tk()
        self.root.title("Sample ChatBot")
        # this removes the maximize
        self.root.resizable(0, 0)

        self.canvas = Canvas(self.root, width=800, height=500, bg="white")
        self.canvas.grid(row=0, column=0)

        self.canvas_scroll_y = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas_scroll_y.grid(row=0, column=1, sticky=(N, S, W, E))

        self.canvas.configure(yscrollcommand=self.canvas_scroll_y.set)
        self.user_input_box = Entry(self.root)
        self.user_input_box.grid(row=1, column=0, padx=5, pady=10, ipady=8, ipadx=290, sticky=W)
        self.user_input_box.bind("<Return>", self.user_input_handler)
        self.user_input_box.bind("<Shift_L><Return>", self.user_input_box_handler)
        send_image = PhotoImage(file=path.join(self.data_path, "send.png"))
        self.bot_image = PhotoImage(file=path.join(self.data_path, "robot.png"))
        self.user_image = PhotoImage(file=path.join(self.data_path, "user.png"))

        self.send_button = Button(self.root, image=send_image,
                                  command=lambda: self.user_input_handler(None))
        self.send_button.grid(row=1, column=0, sticky=E)
        if first_message:
            self.add_bot_message(first_message)
        self.root.mainloop()

    def show_bubble(self, message="", bot=True):
        if self.last_bubble:
            self.canvas.move(ALL, 0, -(self.last_bubble.winfo_height() + 10))
        bg_color = "light blue" if bot else "light grey"
        color = "black"  # if bot else "white"
        frame = Frame(self.canvas, bg=bg_color)
        self.last_bubble = frame
        widget = self.canvas.create_window(50 if bot else 700, 440, window=frame, anchor='nw' if bot else 'ne')

        chat_label = Label(frame, text=message, wraplength=600, justify=LEFT if bot else RIGHT, font=("Helvetica", 12),
                           bg=bg_color, fg=color)
        chat_label.pack(anchor="w" if bot else 'e', side=LEFT if bot else RIGHT, pady=10, padx=10)

        self.root.update_idletasks()
        self.canvas.create_polygon(self.draw_triangle(widget, bot), fill=bg_color, outline=bg_color)
        self.add_icon(widget, bot)

    def add_icon(self, widget, bot=True):
        x1, y1, x2, y2 = self.canvas.bbox(widget)
        if bot:
            self.canvas.create_image(x1 - 72, y2, image=self.bot_image, anchor=W)
        else:
            self.canvas.create_image(x2 + 72, y2, image=self.user_image, anchor=E)

    def draw_triangle(self, widget, bot=True):
        x1, y1, x2, y2 = self.canvas.bbox(widget)
        if bot:
            return x1, y2 - 10, x1 - 10, y2, x1, y2
        return 700, y2 - 10, 700, y2, 710, y2

    def add_user_message(self, message):
        self.user_input_box.config(state=DISABLED)
        self.send_button.config(state=DISABLED)
        self.show_bubble(message, bot=False)
        # need to update canvas scroll region after content modified
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.thread_event.set()

    def process_message(self, message):
        bot_message = self.callback(message)
        while not self.thread_event.is_set():
            sleep(0.1)
        self.add_bot_message(bot_message)

    def add_bot_message(self, message):
        self.show_bubble(message, bot=True)
        self.user_input_box.config(state=NORMAL)
        self.send_button.config(state=NORMAL)
        # need to update canvas scroll region after content modified
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def user_input_handler(self, event):
        message = self.user_input_box.get()

        if not message:
            return

        if message == self.terminate:
            self.root.destroy()
            return

        self.thread_event.clear()
        Thread(target=self.add_user_message, args=(message,)).start()
        Thread(target=self.process_message, args=(message,)).start()
        self.user_input_box.delete(0, END)

    def user_input_box_handler(self, event):
        self.user_input_box.insert(END, "\n")
