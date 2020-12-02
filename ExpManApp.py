import tkinter as tk
from tkinter import*
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import *
from tkcalendar import Calendar, DateEntry
import mysql.connector
from mysql.connector import errorcode
from datetime import date
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database creation
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xIru4114B8GG9 ."
    )
    EMcursor = mydb.cursor()
    EMcursor.execute("CREATE DATABASE ExpManDatabase")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
    elif err.errno == errorcode.ER_DB_CREATE_EXISTS:
        print("Database already exists")
    else:
        print(err)

# Categories table creation
try:
    mydbtbl = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xIru4114B8GG9 .",
        database="ExpManDatabase"
    )
    EMcursor = mydbtbl.cursor()
    EMcursor.execute("CREATE TABLE expenses (year VARCHAR(5),month VARCHAR(2), day VARCHAR (2), aa VARCHAR(255), catg VARCHAR(255), descr VARCHAR(200))")
    EMcursor.execute("CREATE TABLE incomes (year VARCHAR(5),month VARCHAR(2), day VARCHAR (2), aa VARCHAR(255), catg VARCHAR(255), descr VARCHAR(200))")
    EMcursor.execute("CREATE TABLE categories (expense_categ VARCHAR(50), income_categ VARCHAR(50))")
    EMcursor.execute("INSERT INTO categories VALUES ('Other', 'Other'), ('Salary', 'Food'), ('Family', 'Bill'), ('Work', 'Shopping'), ('Scholarchip', 'Transportation')")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
    elif err.errno == errorcode.ER_DB_CREATE_EXISTS:
        print("Database already exists")
    else:
        print(err)


class ExpenseManager(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("800x500")
        self.title("Expense Manager")
        self.title_font = tkfont.Font(family="Arial", size=18, weight="bold", slant="italic")

        def Add_category():
            window = Toplevel(self, bg="#2A2A2A")
            window.geometry("300x200")

            radio_window = tk.Frame(window, bg="#2A2A2A")
            add_window = tk.Frame(window, bg="#2A2A2A")
            button_window = tk.Frame(window, bg="#2A2A2A")
            add_window.place(relx=0.5, rely=0.25, relwidth=0.7, relheight=0.35, anchor="n")
            radio_window.place(relx=0.5, rely=0.1, relwidth=0.7, relheight=0.15, anchor="n")
            button_window.place(relx=0.5, rely=0.7, relwidth=0.7, relheight=0.15, anchor="n")

            var = tk.StringVar()
            radio1 = tk.Radiobutton(radio_window, text="Expenses", variable=var, value="1", indicator=0, bg="#1F1F1F",
                                    fg="#DED4D4", font=("Arial", 13))
            radio2 = tk.Radiobutton(radio_window, text="Incomes", variable=var, value="2", indicator=0, bg="#1F1F1F",
                                    fg="#DED4D4", font=("Arial", 13))
            label = Label(add_window, text = "Category name:", bg = "#2A2A2A", fg = "#FFFFFF", font=('Arial', 13))
            category_entry = tk.Entry(add_window, width=20, bg='#FFFFFF', fg='#2A2A2A', font=('Arial', 13))

            def add():
                category = category_entry.get()
                var2 = var.get()
                if var2 == "2":
                    EMcursor.execute(f"INSERT INTO categories (expense_categ) VALUES ('{category}')")
                elif var2 == "1":
                    EMcursor.execute(f"INSERT INTO categories (income_categ) VALUES ('{category}')")
                mydbtbl.commit()
                window.destroy()

            add_button = tk.Button(button_window, command=add ,text="Add category", width=10, bg='#2A2A2A', fg='#FFFFFF', font=('Arial', 13))
            radio1.pack(side="left", fill="both", expand=True)
            radio2.pack(side="right", fill="both", expand=True)
            label.pack(padx=10, pady=10, side="top", anchor="w")
            category_entry.pack(side="top", anchor="w")
            add_button.pack(side='top', anchor='center')

        # popup messages
        def info():
            messagebox.showwarning("Warning", "We are still working on this")

        def leave():
            answer = messagebox.askyesno("Exit system", "Are you sure you want to quit?")
            if answer:
                self.quit()

        # override the exit button
        self.protocol("WM_DELETE_WINDOW", leave)

        # menubar on all frames
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, font=("Arial", 11))
        file_menu.add_command(label="New entry", command=info)
        file_menu.add_command(label="Chart", command=info)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=leave)
        menubar.add_cascade(label="File", menu=file_menu)

        category_menu = tk.Menu(menubar, tearoff=0, font=("Arial", 11))
        category_menu.add_command(label="Add category", command=Add_category)
        category_menu.add_command(label="Remove category", command=info)
        menubar.add_cascade(label="Categories", menu=category_menu)

        tools_menu = tk.Menu(menubar, tearoff=0, font=("Arial", 11))
        tools_menu.add_radiobutton(label="Light mode", value=1, command=info)
        tools_menu.add_radiobutton(label="Dark mode", value=2, command=info)
        tools_menu.add_separator()
        tools_menu.add_command(label="Settings", command=info)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        help_menu = tk.Menu(menubar, tearoff=0, font=("Arial", 11))
        help_menu.add_command(label="Help", command=info)
        help_menu.add_command(label="Check for updates", command=info)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=info)
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
        d2 = ((date.today()).strftime("%B %d, %Y")).split()
        label = tk.Label(self, text=d2[0], font=controller.title_font,
                         bg="#2A2A2A", fg="#DED4D4")
        label.pack(side="top", fill="x", pady=10)
        # button window
        button_window1 = tk.Frame(self, bg="#2A2A2A")
        button_window1.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor="n")
        # taking info from database
        sumlist = []
        for m in ("incomes", "expenses"):
            EMcursor.execute(f"select * from {m}")
            records = EMcursor.fetchall()
            a = 0
            for row in records:
                today = str(date.today()).split("-")
                if today[0] == row[0]:
                    if today[1] == row[1]:
                        a += float(row[3])
            sumlist = sumlist+[a]
        sumlist = sumlist+[(sumlist[0]-sumlist[1])]

        # buttons on start page
        income_button = tk.Button(button_window1, font=("arial", 13), text="Incomes\n"+str(sumlist[0]), bg="#1F1F1F",
                                  fg="#DED4D4", command=lambda: controller.show_frame("PageIncome"))
        expense_button = tk.Button(button_window1, font=("arial", 13), text="Expenses\n"+str(sumlist[1]), bg="#1F1F1F",
                                   fg="#DED4D4", command=lambda: controller.show_frame("PageExpenses"))
        balance_button = tk.Button(button_window1, font=("arial", 13), text="Balance\n"+str(sumlist[2]), bg="#1F1F1F",
                                   fg="#DED4D4")
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

        # Different windows
        button_window = tk.Frame(self, bg="#2A2A2A")
        sql_window = tk.Frame(self, bg="#2A2A2A")
        diagram_window = tk.Frame(self, bg="#2A2A2A")
        button_window.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor="n")
        sql_window.place(relx=0.08, rely=0.25, relwidth=0.4, relheight=0.7, anchor="nw")
        diagram_window.place(relx=0.53, rely=0.22, relwidth=0.4, relheight=0.62, anchor="nw")
        # Buttons
        first_page_button = tk.Button(button_window, font=("arial", 13), text="<-Back to head page", bg="#1F1F1F",
                                      fg="#DED4D4", command=lambda: controller.show_frame("StartPage"))
        expense_button = tk.Button(button_window, font=("arial", 13), text="Expenses page->", bg="#1F1F1F",
                                   fg="#DED4D4", command=lambda: controller.show_frame("PageExpenses"))
        first_page_button.pack(side="left", fill="both", expand=1)
        expense_button.pack(side="left", fill="both", expand=1)

        # SQL
        textbox = ScrolledText(sql_window, wrap=WORD, bg="#2A2A2A", fg="#DED4D4", width=44, height=23)
        EMcursor.execute("select * from incomes")
        records = EMcursor.fetchall()
        i = 1
        for row in records:
            text1 = f'{i}) {row[2]}.{row[1]}.{row[0]} - {row[3]}€ category: {row[4]} note: {row[5]}\n'
            textbox.insert(END, text1)
            textbox.yview(END)
            i += 1
        textbox.pack(side="left", fill="both", expand=True)

        # Diagram
        fig = matplotlib.figure.Figure(figsize=(4, 4))
        shape = fig.add_subplot(111)
        EMcursor.execute("select * from categories")
        category_records = EMcursor.fetchall()
        categ = []
        for row in category_records:
            categ += [row[0]]
        categories = []
        categories_leg = []
        for i in categ:
            category1 = 0
            for row in records:
                if row[4] == str(i):
                    category1 = category1 + int(row[3])
            if category1 != 0:
                categories += [category1]
                categories_leg += [i]
        # making the pie explode
        explode = []
        for el in categories:
            explode.append(0.05)
        shape.pie(categories, autopct="%1.1f%%", normalize=True, pctdistance=0.78, explode=explode)
        shape.legend(categories_leg,  bbox_to_anchor=(0., 0.02, 1., .102), loc='upper center',
                     ncol=2, mode="expand", borderaxespad=0.)
        circle = matplotlib.patches.Circle((0, 0), 0.4, color="#2A2A2A")
        shape.add_artist(circle)
        canvas = FigureCanvasTkAgg(fig, diagram_window)
        fig.patch.set_facecolor("#2A2A2A")
        canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
        canvas.draw()


class PageExpenses(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#2A2A2A")
        self.controller = controller
        label = tk.Label(self, text="This is page about expenses", font=controller.title_font,
                         bg="#2A2A2A", fg="#DED4D4")
        label.pack(side="top", fill="x", pady=10)

        # Different frames
        button_window = tk.Frame(self, bg="#2A2A2A")
        sql_window = tk.Frame(self, bg="#2A2A2A")
        diagram_window = tk.Frame(self, bg="#2A2A2A")
        button_window.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor="n")
        sql_window.place(relx=0.08, rely=0.25, relwidth=0.4, relheight=0.7, anchor="nw")
        diagram_window.place(relx=0.53, rely=0.22, relwidth=0.4, relheight=0.62, anchor="nw")
        # buttons
        first_page_button = tk.Button(button_window, font=("arial", 13), text="<- Back to head page", bg="#1F1F1F",
                                      fg="#DED4D4", command=lambda: controller.show_frame("StartPage"))
        expense_button = tk.Button(button_window, font=("arial", 13), text="Income page ->", bg="#1F1F1F", fg="#DED4D4",
                                   command=lambda: controller.show_frame("PageIncome"))
        first_page_button.pack(side="left", fill="both", expand=True)
        expense_button.pack(side="left", fill="both", expand=True)

        # SQL
        textbox = ScrolledText(sql_window, wrap=WORD, bg="#2A2A2A", fg="#DED4D4", width=44, height=23)
        EMcursor.execute("select * from expenses")
        records = EMcursor.fetchall()
        i = 1
        categ = ["Food", "Bills", "Shopping", "Clothing", "Travel", "Health", "Other"]
        for row in records:
            text1 = f'{i}) {row[2]}.{row[1]}.{row[0]} - {row[3]}€ category: {row[4]} note: {row[5]}\n'
            textbox.insert(END, text1)
            textbox.yview(END)
            i += 1
        textbox.pack(side="left", fill="both", expand=True)

        # Diagram
        fig = matplotlib.figure.Figure(figsize=(4, 4))
        shape = fig.add_subplot(111)
        EMcursor.execute("select * from categories")
        category_records = EMcursor.fetchall()
        categ = []
        for row in category_records:
            categ += [row[0]]
        categories = []
        categories_leg = []
        for i in categ:
            category1 = 0
            for row in records:
                if row[4] == str(i):
                    category1 = category1 + int(row[3])
            if category1 != 0:
                categories += [category1]
                categories_leg += [i]
        # explosion of pie chart
        explode = []
        for el in categories:
            explode.append(0.05)
        shape.pie(categories, autopct="%1.1f%%", normalize=True, pctdistance=0.78, explode=explode)
        shape.legend(categories_leg,  bbox_to_anchor=(0., 0.02, 1., .102), loc='upper center',
                     ncol=2, mode="expand", borderaxespad=0.)
        circle = matplotlib.patches.Circle((0, 0), 0.4, color="#2A2A2A")
        shape.add_artist(circle)
        canvas = FigureCanvasTkAgg(fig, diagram_window)
        fig.patch.set_facecolor("#2A2A2A")
        canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
        canvas.draw()


class EntryPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#2A2A2A")
        self.controller = controller
        label1 = tk.Label(self, text="Expense/Income insertion page", font=controller.title_font,
                          bg="#2A2A2A", fg="#DED4D4")
        label1.pack(side="top", fill="x", pady=10)

        var = tk.StringVar()
        var_cat = tk.StringVar()

        # different kinds of windows
        button_window = tk.Frame(self, bg="#2A2A2A")
        cancel_window = tk.Frame(self, bg="#2A2A2A")
        category_window = tk.Frame(self, bg="#2A2A2A")
        description_window = tk.Frame(self, bg="#2A2A2A")
        calendar_window = tk.Frame(self, bg="#2A2A2A")
        money_window = tk.Frame(self, bg="#2A2A2A")
        add_window = tk.Frame(self, bg="#2A2A2A")
        button_window.place(relx=0.5, rely=0.1, relwidth=0.7, relheight=0.1, anchor="n")
        cancel_window.place(relx=0.01, rely=0.1, relwidth=0.1, relheight=0.1, anchor="nw")
        category_window.place(relx=0.5, rely=0.25, relwidth=0.4, relheight=0.1, anchor="n")
        description_window.place(relx=0.5, rely=0.4, relwidth=0.7, relheight=0.1, anchor="n")
        calendar_window.place(relx=0.5, rely=0.55, relwidth=0.7, relheight=0.1, anchor="n")
        money_window.place(relx=0.5, rely=0.7, relwidth=0.7, relheight=0.1, anchor="n")
        add_window.place(relx=0.5, rely=0.85, relwidth=0.25, relheight=0.1, anchor="n")

        def expenses_categories():
            for category in bothcategories:
                try:
                    cat_button.menu.delete(f'{category}')
                except:
                    continue
            categories = []
            for row in records:
                categories += [row[1]]
            categories.reverse()
            for category in categories:
                if category != None:
                    cat_button.menu.add_radiobutton(label=category, variable=var_cat, value=category,
                                                    background='#2A2A2A',
                                                    foreground='#FFFFFF', font=('Arial', 12), )
        def incomes_categories():
            for category in bothcategories:
                try:
                    cat_button.menu.delete(f'{category}')
                except:
                    continue
            categories = []
            for row in records:
                categories += [row[0]]
            categories.reverse()
            for category in categories:
                if category != None:
                    cat_button.menu.add_radiobutton(label=category, variable=var_cat, value=category,
                                                    background='#2A2A2A',
                                                    foreground='#FFFFFF', font=('Arial', 12), )

        EMcursor.execute("select * from categories")
        records = EMcursor.fetchall()
        bothcategories = []
        for row in records:
            bothcategories += [row[0]] + [row[1]]
        # different kinds of widgets
        radio1 = tk.Radiobutton(button_window, text="Expenses", variable=var, value="1", indicator=0, bg="#1F1F1F",
                                fg="#DED4D4", font=("Arial", 13), command=expenses_categories)
        radio2 = tk.Radiobutton(button_window, text="Incomes", variable=var, value="2", indicator=0, bg="#1F1F1F",
                                fg="#DED4D4", font=("Arial", 13), command=incomes_categories)
        cancel_button = tk.Button(cancel_window, text='<--', command=lambda: controller.show_frame("StartPage"),
                                  bg="#1F1F1F", fg="#DED4D4")
        cat_button = tk.Menubutton(category_window, text="Categories", bg="#1F1F1F", indicator=0,
                                   fg="#DED4D4", font=("Arial", 13), relief="raised")
        cat_button.menu = Menu(cat_button, tearoff=0, bg="#1F1F1F", fg="#DED4D4")
        cat_button["menu"] = cat_button.menu
        desc_label = tk.Label(description_window, text='             Enter Memo              ', bg='#2A2A2A',
                              fg='#DED4D4', font=('Arial', 13))
        description = tk.Entry(description_window, width=20, bg='#FFFFFF', fg='#2A2A2A', font=('Arial', 14))
        cal_label = tk.Label(calendar_window, text='Choose date', bg='#2A2A2A', fg='#DED4D4', font=('Arial', 13))
        cal = DateEntry(calendar_window, width=12, bg="#1F1F1F", fg='#DED4D4', borderwidth=2)
        money_label = tk.Label(money_window, text='             Enter the amount      ', bg='#2A2A2A',
                               fg='#DED4D4', font=('Arial', 13))
        smma = tk.Entry(money_window, width=20, bg='#FFFFFF', fg='#2A2A2A', font=('Arial', 14))
        radio1.pack(side="left", fill="both", expand=True)
        radio2.pack(side="right", fill="both", expand=True)
        cancel_button.pack(side="left", fill="both", expand=True)
        cat_button.pack(side="left", fill="both", expand=True)
        desc_label.pack(side="left", fill="both", expand=True)
        description.pack(side="left", fill="both", expand=True)
        cal_label.pack(side="left", fill="both", expand=True)
        cal.pack(side="left", fill="both", expand=True)
        money_label.pack(side="left", fill="both", expand=True)
        smma.pack(side="left", fill="both", expand=True)

        def intodb():
            var2 = var.get()
            caldate = str(cal.get_date()).split("-")
            sma = str(smma.get())
            category2 = var_cat.get()
            note = description.get()
            if var2 == "1":
                EMcursor.execute(f"INSERT INTO expenses VALUES ({caldate[0]}, {caldate[1]}, {caldate[2]}, {sma}, '{category2}', '{note}')")
            elif var2 == "2":
                EMcursor.execute(f"INSERT INTO incomes VALUES ({caldate[0]}, {caldate[1]}, {caldate[2]}, {sma}, '{category2}', '{note}')")
            mydbtbl.commit()
            controller.show_frame("StartPage")

        add_button = tk.Button(add_window, text='Add', command=intodb, bg="#1F1F1F", fg="#DED4D4")
        add_button.pack(side="top", fill="both", expand=True)


if __name__ == "__main__":
    app = ExpenseManager()
    app.mainloop()
