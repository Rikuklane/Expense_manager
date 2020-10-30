import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from tkcalendar import Calendar, DateEntry


class ExpenseManager(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("800x500")
        self.title("Expense Manager")
        self.title_font = tkfont.Font(family="Arial", size=18, weight="bold", slant="italic")

        # menubar on all frames
        def hello():
            print("Hello!")

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, font=("Arial", 11))
        file_menu.add_command(label="New entry", command=hello)
        file_menu.add_command(label="Chart", command=hello)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        category_menu = tk.Menu(menubar, tearoff=0, font=("Arial", 11))
        category_menu.add_command(label="Add category", command=hello)
        category_menu.add_command(label="Remove category", command=hello)
        menubar.add_cascade(label="Categories", menu=category_menu)

        tools_menu = tk.Menu(menubar, tearoff=0, font=("Arial", 11))
        tools_menu.add_radiobutton(label="Light mode", value=1)
        tools_menu.add_radiobutton(label="Dark mode", value=2)
        tools_menu.add_separator()
        tools_menu.add_command(label="Settings", command=hello)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        help_menu = tk.Menu(menubar, tearoff=0, font=("Arial", 11))
        help_menu.add_command(label="Help", command=hello)
        help_menu.add_command(label="Check for updates", command=hello)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=hello)
        menubar.add_cascade(label="Help", menu=help_menu)

        # the container is where we stack frames on top of each other. Wanted page will raise above the others.
        container = tk.Frame(self, bg="#2A2A2A")
        container.place(relwidth=1, relheight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (EntryPage, StartPage, PageIncome, PageExpenses):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location on top of each other. Top one is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#2A2A2A")
        self.controller = controller
        label = tk.Label(self, text="November", font=controller.title_font,
                         bg="#2A2A2A", fg="#DED4D4")
        label.pack(side="top", fill="x", pady=10)

        # button window
        button_window1 = tk.Frame(self, bg="#2A2A2A")
        button_window1.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor="n")
        income_button = tk.Button(button_window1, font=("arial", 13), text="Income\n0.00", bg="#1F1F1F", fg="#DED4D4",
                                  command=lambda: controller.show_frame("PageIncome"))
        expense_button = tk.Button(button_window1, font=("arial", 13), text="Expenses\n0.00", bg="#1F1F1F",
                                   fg="#DED4D4", command=lambda: controller.show_frame("PageExpenses"))
        balance_button = tk.Button(button_window1, font=("arial", 13), text="Balance\n0.00", bg="#1F1F1F", fg="#DED4D4")
        income_button.pack(side="left", fill="both", expand=True)
        expense_button.pack(side="left", fill="both", expand=True)
        balance_button.pack(side="left", fill="both", expand=True)

        button_window2 = tk.Frame(self, bg="#2A2A2A")
        button_window2.place(relx=0.9, rely=0.9, relwidth=0.2, relheight=0.1, anchor="n")
        entry_button = tk.Button(button_window2, font=("arial", 13), text="Add an entry", bg="#1F1F1F",
                                 fg="#DED4D4", command=lambda: controller.show_frame("EntryPage"))
        entry_button.pack(side="left", fill="both", expand=True)


class PageIncome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#2A2A2A")
        self.controller = controller
        label = tk.Label(self, text="This is page about incomes", font=controller.title_font,
                         bg="#2A2A2A", fg="#DED4D4")
        label.pack(side="top", fill="x", pady=10)

        # button window
        button_window = tk.Frame(self, bg="#2A2A2A")
        button_window.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor="n")
        first_page_button = tk.Button(button_window, font=("arial", 13), text="<- Back to head page", bg="#1F1F1F",
                                      fg="#DED4D4", command=lambda: controller.show_frame("StartPage"))
        expense_button = tk.Button(button_window, font=("arial", 13), text="Expenses page ->", bg="#1F1F1F",
                                   fg="#DED4D4", command=lambda: controller.show_frame("PageExpenses"))
        first_page_button.pack(side="left", fill="both", expand=True)
        expense_button.pack(side="left", fill="both", expand=True)


class PageExpenses(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#2A2A2A")
        self.controller = controller
        label = tk.Label(self, text="This is page about expenses", font=controller.title_font,
                         bg="#2A2A2A", fg="#DED4D4")
        label.pack(side="top", fill="x", pady=10)

        # button window
        button_window = tk.Frame(self, bg="#2A2A2A")
        button_window.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor="n")
        first_page_button = tk.Button(button_window, font=("arial", 13), text="<- Back to head page", bg="#1F1F1F",
                                      fg="#DED4D4", command=lambda: controller.show_frame("StartPage"))
        expense_button = tk.Button(button_window, font=("arial", 13), text="Income page ->", bg="#1F1F1F", fg="#DED4D4",
                                   command=lambda: controller.show_frame("PageIncome"))
        first_page_button.pack(side="left", fill="both", expand=True)
        expense_button.pack(side="left", fill="both", expand=True)


class EntryPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#2A2A2A")
        self.controller = controller
        label = tk.Label(self, text="Expense insertion page", font=controller.title_font,
                         bg="#2A2A2A", fg="#DED4D4")
        label.pack(side="top", fill="x", pady=10)

        def calendar():
            top = tk.Toplevel(self)

            ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

            cal = DateEntry(top, width=12, background='#2A2A2A',
                            foreground='#DED4D4', borderwidth=2)
            cal.pack(padx=10, pady=10)

        s = ttk.Style(self)
        s.theme_use('clam')

        ttk.Button(self, text='DateEntry', command=calendar).pack(padx=10, pady=10)


if __name__ == "__main__":
    app = ExpenseManager()
    app.mainloop()
