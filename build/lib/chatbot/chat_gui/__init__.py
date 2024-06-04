from os import path
from tkinter import Tk, Canvas, Frame, Label, \
    ALL, Button, Entry, END, Scrollbar, N, S, E, W, LEFT, PhotoImage
from tkinter.constants import DISABLED, NORMAL, RIGHT
from threading import Thread, Event
from time import sleep


class ChatGUI:
    def __init__(self, callback, first_message="welcome to ChatBotAI", terminate="quit"):
        """
        callback: (function) Bot callback function
        first_message: (Str) first string message show to user
        terminate: (str) string message shown user

        Initialize the tkinter window and start the mainloop.

        Canvas is used to create the window. Each message is created as
        """
        # media path for bot images
        self.data_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), "media")

        # instance args
        self.callback = callback
        self.terminate = terminate

        # initialize tkinter start
        self.root = Tk()
        self.root.title("Sample ChatBot")
        self.root.protocol("WM_DELETE_WINDOW", self.close_handler)
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
        self.send_button = Button(self.root, image=send_image,
                                  command=lambda: self.user_input_handler(None))
        self.send_button.grid(row=1, column=0, sticky=E)

        self.bot_image = PhotoImage(file=path.join(self.data_path, "robot.png"))
        self.user_image = PhotoImage(file=path.join(self.data_path, "user.png"))
        # initialize tkinter stop

        # get the last bubble objects to move them up for next bubbles
        self.last_bubble = None

        # bubble thread objects
        self.user_thread = None
        self.bot_thread = None
        self.thread_event = Event()

        if first_message:
            self.add_bot_message(first_message)

        self.root.mainloop()

    def close_handler(self):
        """
        When the close button of MainWindow pressed we need to kill the active threads
        before closing the window.
        """
        if self.user_thread and self.user_thread.is_alive():
            self.bot_thread._tstate_lock.release_lock()
            self.user_thread._stop()
        if self.bot_thread and self.bot_thread.is_alive():
            self.bot_thread._tstate_lock.release_lock()
            self.bot_thread._stop()
        self.root.destroy()

    def show_bubble(self, message="", bot=True):
        """
        message: (str) Bubble message shown in canvas
        bot: (bool) Shown the bubble based on this value

        Add the bubble to canvas.

        Previous canvas are moved based on the last bubble height and new bubbles are added.
        Color, arrow(draw_triangle), image(add_icon) and Position of the Bubble is configures here

        UserBubble is added to right side of the canvas.
        BotBubble is added to left side of the canvas.
        """
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
        """
        Add the image to given widget.
        Currently this based bot and user bubble positions.

        If it's moved we need to update the x1 and y1 values.
        """
        x1, y1, x2, y2 = self.canvas.bbox(widget)
        if bot:
            self.canvas.create_image(x1 - 72, y2, image=self.bot_image, anchor=W)
        else:
            self.canvas.create_image(x2 + 72, y2, image=self.user_image, anchor=E)

    def draw_triangle(self, widget, bot=True):
        """
        Draw the triangles in the bubble widget.
        """
        x1, y1, x2, y2 = self.canvas.bbox(widget)
        if bot:
            return x1, y2 - 10, x1 - 10, y2, x1, y2
        return 700, y2 - 10, 700, y2, 710, y2

    def add_user_message(self, message):
        """
        create a user bubble and disable the input box until bot bubble is shown.
        Moreover, update the scroll location of the canvas
        """
        self.user_input_box.config(state=DISABLED)
        self.send_button.config(state=DISABLED)
        self.show_bubble(message, bot=False)
        # need to update canvas scroll region after content modified
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.thread_event.set()

    def add_bot_message(self, message):
        """
        create a bot bubble and enable the input box after message shown in the canvas.
        Moreover, update the scroll location of the canvas
        """
        self.show_bubble(message, bot=True)
        self.user_input_box.config(state=NORMAL)
        self.send_button.config(state=NORMAL)
        # need to update canvas scroll region after content modified
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def process_message(self, message):
        """
        Call the bot handler and add the result to bot_message
        """
        bot_message = self.callback(message)
        while not self.thread_event.is_set():
            sleep(0.1)
        self.add_bot_message(bot_message)

    def user_input_handler(self, event):
        """
        User InputBox widget
        """
        message = self.user_input_box.get()

        if not message:
            return

        if message == self.terminate:
            self.close_handler()
            return

        self.thread_event.clear()
        self.user_thread = Thread(target=self.add_user_message, args=(message,))
        self.bot_thread = Thread(target=self.process_message, args=(message,))
        self.user_thread.start()
        self.bot_thread.start()

        self.user_input_box.delete(0, END)

    def user_input_box_handler(self, event):
        """
        Helper method to add the newline in the InputBox
        """
        self.user_input_box.insert(END, "\n")
