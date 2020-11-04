import tkinter as tk
from tkinter import*
from tkinter import font as tkfont
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import mysql.connector
from datetime import date
from tkinter import messagebox
from tkinter.scrolledtext import*
from mysql.connector import errorcode

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"
    )
    EMcursor = mydb.cursor()
    EMcursor.execute("CREATE DATABASE ExpManDatabase")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_DB_CREATE_EXISTS:
        print("Database already exists")
    else:
        print(err)
try:
    mydbtbl = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ExpManDatabase"
    )
    EMcursor = mydbtbl.cursor()
    EMcursor.execute("CREATE TABLE expenses (year VARCHAR(255),month VARCHAR(255), day VARCHAR (255), aa VARCHAR(255))")
    EMcursor.execute("CREATE TABLE incomes (year VARCHAR(200),month VARCHAR(200), day VARCHAR (200), aa VARCHAR(200))")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
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

        # popup messages
        def info():
            messagebox.showwarning("Warning", "We are still working on this")

        def leave():
            answer = messagebox.askyesno("Exit system", "Are you sure you want to quit?")
            if answer:
                self.quit()

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
        category_menu.add_command(label="Add category", command=info)
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
        #taking info from database
        sumlist=[]
        for m in ("expenses", "incomes"):
            sql_select = "select * from %s"%m
            EMcursor.execute(sql_select)
            records = EMcursor.fetchall()
            a=0
            for row in records:
                today=str(date.today()).split("-")
                if today[0]==row[0]:
                    if today[1]==row[1]:
                        a+=float(row[3])
            sumlist=sumlist+[a]
        sumlist=sumlist+[(sumlist[0]-sumlist[1])]
        #buttons
        income_button = tk.Button(button_window1, font=("arial", 13), text="Incomes\n"+str(sumlist[0]), bg="#1F1F1F", fg="#DED4D4",
                                  command=lambda: controller.show_frame("PageIncome"))
        expense_button = tk.Button(button_window1, font=("arial", 13), text="Expenses\n"+str(sumlist[1]), bg="#1F1F1F",
                                   fg="#DED4D4", command=lambda: controller.show_frame("PageExpenses"))
        balance_button = tk.Button(button_window1, font=("arial", 13), text="Balance\n"+str(sumlist[2]), bg="#1F1F1F", fg="#DED4D4")
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
        first_page_button = tk.Button(button_window, font=("arial", 13), text="<-Back to head page", bg="#1F1F1F",
                                      fg="#DED4D4", command=lambda: controller.show_frame("StartPage"))
        expense_button = tk.Button(button_window, font=("arial", 13), text="Expenses page->", bg="#1F1F1F",
                                   fg="#DED4D4", command=lambda: controller.show_frame("PageExpenses"))
        first_page_button.pack(side="left", fill="both", expand=1)
        expense_button.pack(side="left", fill="both", expand=1)

        textbox=ScrolledText(self, wrap=WORD, bg="#2A2A2A", fg="#DED4D4", width=44, height= 23)
        sql_select = "select * from incomes"
        EMcursor.execute(sql_select)
        records = EMcursor.fetchall()
        i = 1
        for row in records:
            text1 = str(i) + ") " + row[2] + "." + row[1] + "." + row[0] + " - " + row[3] + "€" + "\n"
            textbox.insert(END, text1)
            textbox.yview(END)
            i += 1
        textbox.pack(anchor="sw", side="bottom", padx=38, pady=20)
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

        textbox = ScrolledText(self, wrap=WORD, bg="#2A2A2A", fg="#DED4D4", width=44, height=23)
        sql_select = "select * from expenses"
        EMcursor.execute(sql_select)
        records = EMcursor.fetchall()
        i = 1
        for row in records:
            text1 = str(i) + ") " + row[2] + "." + row[1] + "." + row[0] + " - " + row[3] + "€" + "\n"
            textbox.insert(END, text1)
            textbox.yview(END)
            i += 1
        textbox.pack(anchor="sw", side="bottom", padx=38, pady=20)

class EntryPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#2A2A2A")
        self.controller = controller
        label = tk.Label(self, text="Expense insertion page", font=controller.title_font,
                         bg="#2A2A2A", fg="#DED4D4")
        label.pack(side="top", fill="x", pady=10)

        s = ttk.Style(self)
        s.theme_use('clam')

        var = tk.StringVar()
        r1 = tk.Radiobutton(self, text="Expenses", variable= var, value="1", indicator=0, background="#2A2A2A", foreground="#DED4D4", font=("Arial", 12))
        r1.pack(fill="x", ipady=5)
        r2 = tk.Radiobutton(self, text="Incomes", variable= var, value="2", indicator=0, background="#2A2A2A", foreground="#DED4D4", font=("Arial", 12))
        r2.pack(fill="x", ipady=5)
        ttk.Label(self, text='Choose date', background='#2A2A2A', foreground='#DED4D4', font=('Arial', 13)).pack(padx=10, pady=10)
        cal = DateEntry(self, width=12, background='#2A2A2A', foreground='#DED4D4', borderwidth=2)
        cal.pack(padx=10, pady=10, anchor="center")
        ttk.Label(self, text='Ma ei tea nh, siia summa', background='#2A2A2A', foreground='#DED4D4', font=('Arial', 13)).pack(padx=10, pady=10)
        smma = ttk.Entry(self, width=20, background='#DAD4D4', foreground='#2A2A2A')
        smma.pack(padx=10, pady=5)

        def intodb():
            var2 = var.get()
            caldate = str(cal.get_date()).split("-")
            sma = str(smma.get())
            if var2 == "1":
                expenses_sql = "INSERT INTO expenses (year, month, day, aa) VALUES (%s, %s, %s, %s)" % (caldate[0], caldate[1], caldate[2], sma)
                EMcursor.execute(expenses_sql)
            elif var2 == "2":
                incomes_sql = "INSERT INTO incomes (year, month, day, aa) VALUES (%s, %s, %s, %s)" % (caldate[0], caldate[1], caldate[2], sma)
                EMcursor.execute(incomes_sql)
            mydbtbl.commit()
            controller.show_frame("StartPage")

        ttk.Button(self, text='Add', command=intodb).pack(padx=10, pady=10)


if __name__ == "__main__":
    app = ExpenseManager()
    app.mainloop()
