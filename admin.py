import sqlite3
import random
import string
import re
from tkinter import *
from tkinter import messagebox, ttk
from tkinter import scrolledtext as tkst
from datetime import date
from time import strftime

root = Tk()
root.geometry("1366x768")
root.title("Welcome Admin 👋")

user = StringVar()      # StringVar() : A class that is used to store a string value
pswd = StringVar()
first_name = StringVar()
last_name = StringVar()

# Connecting to the database and creating a cursor object
with sqlite3.connect("./database/clinicDatabase.db") as db:
    # Using cursors, we can invoke methods that execute SQLite statements, fetch data from the result sets of the queries.
    cur = db.cursor()

def generate_employee_id(length):
    """
    It takes a length as an argument and returns a string of that length with the first three characters being 'DTC' and the rest being random numbers
    
    :param length: The length of the ID you want to generate
    :return: A string of random numbers
    """
    dig = string.digits
    random_numbers = ''.join(random.choice(dig) for i in range(length - 3))
    return('DTC' + random_numbers)

def is_valid_phone(phone_number):
    """
    It checks if the given phone number is valid or not
    
    :param phone_number: The phone number to validate
    :return: True or False
    """
    if re.match(r"^[6-9]\d{9}$", phone_number):
        return True
    return False

def is_valid_aadhar(aadhar_number):
    """
    If the aadhar_number is a digit and has a length of 12, return True, otherwise return False
    
    :param aadhar_number: The Aadhar number to be validated
    :return: True or False
    """
    if aadhar_number.isdigit() and len(aadhar_number) == 12:
        return True
    return False


class LoginPage:
    def __init__(self, top=None):
        # The Toplevel widget is used to create and display the toplevel windows which are directly managed by the window manager
        top.geometry("1366x768")
        top.resizable(0, 0)         # To create a fixed size window
        top.title("Dr.Teeth Dental Clinic Admin")

        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/admin_login.png")
        self.label1.configure(image=self.img)
        
        # Creating a text entry box and placing it on the screen.
        self.entry1 = Entry(root)       # A widget that is used to enter text strings
        self.entry1.place(relx=0.350, rely=0.330, width=374, height=40)
        self.entry1.configure(font="-family {Bookman Old Style} -size 18")
        # The relief style of a widget refers to certain simulated 3-D effects around the outside of the widget (Reference : https://www.tutorialspoint.com/python3/tk_relief.htm)
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)

        # Creating a text entry box and placing it on the screen.
        self.entry2 = Entry(root)
        self.entry2.place(relx=0.350, rely=0.530, width=374, height=40)
        self.entry2.configure(font="-family {Bookman Old Style} -size 18")
        self.entry2.configure(relief="flat")
        self.entry2.configure(show="*")
        self.entry2.configure(textvariable=pswd)

        # Creating a button and placing it on the screen.
        self.button1 = Button(root)
        self.button1.place(relx=0.42, rely=0.7525, width=225, height=65)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#405763")
        self.button1.configure(cursor="hand2")          # Changing the cursor to a hand when the mouse is over the button
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#405763")
        self.button1.configure(font="-family {Bookman Old Style} -weight {bold} -size 20")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""LOGIN""")
        self.button1.configure(command=self.login)
    
    def login(self, Event=None):
        username = user.get()
        password = pswd.get()

        # Connecting to the database and creating a cursor object
        with sqlite3.connect("./database/clinicDatabase.db") as db:
            # Using cursors, we can invoke methods that execute SQLite statements, fetch data from the result sets of the queries.
            cur = db.cursor()

        # A SQL query that is used to fetch the data from the database.
        find_login_credentials = "SELECT * FROM employee WHERE employee_id = ? and password = ?"
        cur.execute(find_login_credentials, [username, password])
        result = cur.fetchall()
        
        if result:
            if result[0][6] == "Admin":
                messagebox.showinfo("Login Page", "Login successful ✔️")
                # Deleting the text in the entry boxes, after the button has been pressed.
                page1.entry1.delete(0, END)
                page1.entry2.delete(0, END)

                root.withdraw()     # Hiding the root window.

                global admin
                global page2
                admin = Toplevel()      # The Toplevel widget is used to create and display the toplevel windows which are directly managed by the window manager. It is used when a python application needs to represent some extra information, pop-up, or the group of widgets on the new window.
                page2 = AdminPage(admin)
                admin.protocol("WM_DELETE_WINDOW", exit)
                admin.mainloop()    # mainloop() : This method listens for events, such as button clicks or keypresses, and blocks any code that comes after it from running until you close the window where you called the method.
            else:
                messagebox.showerror("Oops!!", "You are not an admin ❌")

        else:
            messagebox.showerror("Error!!", "Incorrect username or password ❌")
            page1.entry2.delete(0, END)
    
def exit():
    """
    If the user clicks the "Yes" button, the program will close. If the user clicks the "No" button, the program will not close.
    """
    exit_confirmation = messagebox.askyesno("Exit", "Are you sure, you want to exit ?", parent=root)
    if exit_confirmation == True:
        admin.destroy()
        root.destroy()

def employees():
    """
    It hides the admin window and opens the employee window.
    """
    admin.withdraw()        # Hiding the admin window
    global emp
    global page3
    emp = Toplevel()
    page3 = EmployeePage(emp)
    page3.time()
    emp.protocol("WM_DELETE_WINDOW", exit)
    emp.mainloop()

def invoices():
    """
    It hides the admin window and opens the invoices window.
    """
    admin.withdraw()        # Hiding the admin window
    global inv
    inv = Toplevel()
    page4 = InvoicesPage(inv)
    page4.time()
    inv.protocol("WM_DELETE_WINDOW", exit)
    inv.mainloop()


class AdminPage:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Admin Mode")

        self.label1 = Label(admin)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/admin.png")
        self.label1.configure(image=self.img)

        self.button1 = Button(admin)        # Creating a button and placing it on the screen.
        self.button1.place(relx=0.02, rely=0.120, width=200, height=45)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#20212e")
        self.button1.configure(cursor="hand2")      # Changing the cursor to a hand when the mouse is over the button
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#20212e")
        self.button1.configure(font="-family {Bookman Old Style} -weight {bold} -size 18")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""LOGOUT""")
        self.button1.configure(command=self.logout)

        self.button2 = Button(admin)
        self.button2.place(relx=0.2175, rely=0.708, width=180, height=63)
        self.button2.configure(relief="raised")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#112124")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#112124")
        self.button2.configure(font="-family {Bookman Old Style} -weight {bold} -size 18")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""EMPLOYEES""")
        self.button2.configure(command=employees)

        self.button4 = Button(admin)
        self.button4.place(relx=0.665, rely=0.708, width=146, height=63)
        self.button4.configure(relief="raised")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#112124")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#112124")
        self.button4.configure(font="-family {Bookman Old Style} -weight {bold} -size 18")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""INVOICES""")
        self.button4.configure(command=invoices)

    def logout(self):
        sure = messagebox.askyesno("Logout", "Sure, you want to logout ?", parent=admin)
        if sure == True:
            admin.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


page1 = LoginPage(root)
root.bind("<Return>", LoginPage.login)
root.mainloop()
