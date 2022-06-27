from operator import ge
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
root.title("Receptionist")

user = StringVar()
pswd = StringVar()

patient_bill_number = StringVar()
doctor_name = StringVar()
patient_name = StringVar()
patient_mobile_number = StringVar()
bill_amount = StringVar()
bill_date = StringVar()

# Connecting to the database and creating a cursor object
with sqlite3.connect("./database/clinicDatabase.db") as db:
    # Using cursors, we can invoke methods that execute SQLite statements, fetch data from the result sets of the queries.
    cur = db.cursor()

def generate_random_bill_number(length):
    """
    It takes a length as an argument and returns a string of that length with the first three characters being 'BTD' and the rest being random letters and numbers
    
    :param length: The length of the string you want to generate
    :return: A string of length 'length' with the first two characters being 'BTD'
    """
    letters_and_digits = string.ascii_letters.upper() + string.digits
    str = ''.join(random.choice(letters_and_digits) for i in range(length - 3))
    return ('BTD' + str)

def is_valid_phone(phone_number):
    """
    It checks if the given phone number is valid or not
    
    :param phone_number: The phone number to validate
    :return: True or False
    """
    if re.match(r"^[6-9]\d{9}$", phone_number):
        return True
    return False

def login(Event=None):
    """
    It checks if the username and password entered by the user are correct. If they are, it opens a new window
    
    :param Event: This is the event that is passed to the function
    """
    global username
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
        messagebox.showinfo("Login Page", "The login is successful")
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)

        root.withdraw()
        
        global bills_ledger
        global page2
        bills_ledger = Toplevel()
        page2 = ReceiptGeneratePage(bills_ledger)
        page2.time()
        bills_ledger.protocol("WM_DELETE_WINDOW", exit)
        bills_ledger.mainloop()
    else:
        messagebox.showerror("Error", "Incorrect username or password")
        page1.entry2.delete(0, END)

def logout():
    """
    If the user clicks "Yes" on the messagebox, the bills_ledger window is destroyed and the root window is
    deiconified.
    """
    logout_confirmation = messagebox.askyesno("Logout", "Are you sure you want to logout ?", parent=bills_ledger)
    if logout_confirmation == True:
        bills_ledger.destroy()
        root.deiconify()
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)


class LoginPage:
    def __init__(self, top=None):
        # The Toplevel widget is used to create and display the toplevel windows which are directly managed by the window manager.
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Retail Manager")

        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/receptionist_login.png")
        self.label1.configure(image=self.img)

        # Creating a text entry box and placing it on the screen.
        self.entry1 = Entry(root)       # A widget that is used to enter text strings
        self.entry1.place(relx=0.350, rely=0.36, width=374, height=40)
        self.entry1.configure(font="-family {Cambria Math} -size 18")
        # The relief style of a widget refers to certain simulated 3-D effects around the outside of the widget (Reference : https://www.tutorialspoint.com/python3/tk_relief.htm)
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)

        # Creating a text entry box and placing it on the screen.
        self.entry2 = Entry(root)
        self.entry2.place(relx=0.350, rely=0.54, width=374, height=40)
        self.entry2.configure(font="-family {Cambria Math} -size 18")
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
        self.button1.configure(command=login)

def exit():
    """
    If the user clicks the "Yes" button, the bills_ledger window is destroyed and the root window is
    destroyed.
    """
    exit_confirmation = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=bills_ledger)
    if exit_confirmation == True:
        bills_ledger.destroy()
        root.destroy()


class ReceiptGeneratePage:
    def __init__(self, top=None):
        """
        It creates a window with a background image and some buttons and text boxes.
        
        :param top: The window that is being created
        """
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Welcome Receptionist")

        # Creating a label and placing it on the window.
        self.label = Label(bills_ledger)
        self.label.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/receipt_window.png")
        self.label.configure(image=self.img)

        # Creating a label widget and placing it on the window.
        self.message = Label(bills_ledger)
        self.message.place(relx=0.06, rely=0.065, width=136, height=30)
        self.message.configure(font="-family {Cambria} -size 14")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text=username)
        self.message.configure(anchor="w")

        # Creating a label widget and placing it on the window.
        self.clock = Label(bills_ledger)
        self.clock.place(relx=0.85, rely=0.065, width=140, height=36)
        self.clock.configure(font="-family {Cambria Math} -size 14")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        # Creating a text box for the receptionist to enter the doctor's name.
        self.entry1 = Entry(bills_ledger)
        self.entry1.place(relx=0.1675, rely=0.335, width=240, height=24)
        self.entry1.configure(font="-family {Cambria Math} -size 14")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=doctor_name)

        # Creating a text box for the receptionist to enter the patient name.
        self.entry2 = Entry(bills_ledger)
        self.entry2.place(relx=0.175, rely=0.4225, width=240, height=24)
        self.entry2.configure(font="-family {Cambria Math} -size 14")
        self.entry2.configure(relief="flat")
        self.entry2.configure(textvariable=patient_name)

        # Creating a text box for the user to enter the mobile number of the patient.
        self.entry3 = Entry(bills_ledger)
        self.entry3.place(relx=0.235, rely=0.5125, width=150, height=24)
        self.entry3.configure(font="-family {Cambria Math} -size 14")
        self.entry3.configure(relief="flat")
        self.entry3.configure(textvariable=patient_mobile_number)

        # Creating a text box for the user to enter the amount of the bill.
        self.entry4 = Entry(bills_ledger)
        self.entry4.place(relx=0.135, rely=0.6, width=240, height=24)
        self.entry4.configure(font="-family {Cambria Math} -size 14")
        self.entry4.configure(relief="flat")
        self.entry4.configure(textvariable=bill_amount)

        # Creating a button and placing it on the screen.
        self.button1 = Button(bills_ledger)
        self.button1.place(relx=0.0375, rely=0.115, width=90, height=27.5)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#20212e")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#20212e")
        self.button1.configure(font="-family {Bookman Old Style} -weight {bold} -size 12")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""LOGOUT""")
        self.button1.configure(command=logout)

        # Creating a button and placing it on the window.
        self.button2 = Button(bills_ledger)
        self.button2.place(relx=0.062, rely=0.8075, width=100, height=30)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Comic Sans MS} -weight {bold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""GENERATE""")
        self.button2.configure(command=self.generate_receipt)

        # Creating a button with the text "CLEAR" and when clicked it will call the function clear_bill.
        self.button3 = Button(bills_ledger)
        self.button3.place(relx=0.175, rely=0.8075, width=100, height=30)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Comic Sans MS} -weight {bold} -size 14")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""CLEAR""")
        self.button3.configure(command=self.clear_bill)

        # Creating a button that will exit the program.
        self.button4 = Button(bills_ledger)
        self.button4.place(relx=0.285, rely=0.8075, width=100, height=30)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Comic Sans MS} -weight {bold} -size 14")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""EXIT""")
        self.button4.configure(command=exit)

    def fill_details_into_billWindow(self):
        """
        It fills the details of the bill into the bill window.
        """
        # Creating a text widget and placing it in the bills_ledger window.
        self.bill_number_msg = Text(bills_ledger)
        self.bill_number_msg.place(relx=0.51, rely=0.491, width=150, height=30)
        self.bill_number_msg.configure(font="-family {Courier} -size 12")
        self.bill_number_msg.configure(borderwidth=0)
        self.bill_number_msg.configure(background="#ffffff")

        # Creating a text widget and placing it in the bills_ledger window.
        self.patient_name_msg = Text(bills_ledger)
        self.patient_name_msg.place(relx=0.7725, rely=0.491, width=150, height=30)
        self.patient_name_msg.configure(font="-family {Courier} -size 12")
        self.patient_name_msg.configure(borderwidth=0)
        self.patient_name_msg.configure(background="#ffffff")

        # Creating a text widget and placing it in the bills_ledger window.
        self.doctor_name_msg = Text(bills_ledger)
        self.doctor_name_msg.place(relx=0.51, rely=0.5875, width=150, height=30)
        self.doctor_name_msg.configure(font="-family {Courier} -size 12")
        self.doctor_name_msg.configure(borderwidth=0)
        self.doctor_name_msg.configure(background="#ffffff")

        # Creating a text widget and placing it in the bills_ledger window.
        self.patient_mobile_msg = Text(bills_ledger)
        self.patient_mobile_msg.place(relx=0.825, rely=0.5875, width=150, height=30)
        self.patient_mobile_msg.configure(font="-family {Courier} -size 12")
        self.patient_mobile_msg.configure(borderwidth=0)
        self.patient_mobile_msg.configure(background="#ffffff")

        # Creating a text widget and placing it in the bills_ledger window.
        self.bill_date_msg = Text(bills_ledger)
        self.bill_date_msg.place(relx=0.715, rely=0.7575, width=150, height=30)
        self.bill_date_msg.configure(font="-family {Courier} -size 12")
        self.bill_date_msg.configure(borderwidth=0)
        self.bill_date_msg.configure(background="#ffffff")

        # Creating a text widget and placing it in the bills_ledger window.
        self.bill_amount_msg = Text(bills_ledger)
        self.bill_amount_msg.place(relx=0.7275, rely=0.812, width=150, height=30)
        self.bill_amount_msg.configure(font="-family {Courier} -size 12")
        self.bill_amount_msg.configure(borderwidth=0)
        self.bill_amount_msg.configure(background="#ffffff")

    def generate_receipt(self):
        """
        It generates a receipt for the patient.
        """
        self.fill_details_into_billWindow()

        if(doctor_name.get() == ""):
            messagebox.showerror("Oops!", "Please enter doctor name.", parent=bills_ledger)
        elif(patient_name.get() == ""):
            messagebox.showerror("Oops!", "Please enter patient number.", parent=bills_ledger)
        elif is_valid_phone(patient_mobile_number.get()) == False:
            messagebox.showerror("Oops!", "Please enter patient's valid mobile number.", parent=bills_ledger)
        elif(bill_amount.get() == ""):
            messagebox.showerror("Oops!", "Please enter bill amount.", parent=bills_ledger)
        else: 
            # Generating a random number and inserting it into the text box.
            patient_bill_number.set(generate_random_bill_number(8))
            self.bill_number_msg.insert(END, patient_bill_number.get())
            self.bill_number_msg.configure(state="disabled")

            # Inserting the value of the variable doctor_name into the text box.
            self.doctor_name_msg.insert(END, doctor_name.get())
            self.doctor_name_msg.configure(state="disabled")

            # Inserting the value of the patient_name variable into the patient_name_msg widget.
            self.patient_name_msg.insert(END, patient_name.get())
            self.patient_name_msg.configure(state="disabled")

            # Inserting the value of the variable patient_mobile_number into the text box.
            self.patient_mobile_msg.insert(END, patient_mobile_number.get())
            self.patient_mobile_msg.configure(state="disabled")

            # Setting the date to today's date.
            bill_date.set(str(date.today()))
            self.bill_date_msg.insert(END, bill_date.get())
            self.bill_date_msg.configure(state="disabled")

            # Inserting the value of bill_amount into the bill_amount_msg text box.
            self.bill_amount_msg.insert(END, bill_amount.get())
            self.bill_amount_msg.configure(state="disabled")

            # Inserting the values into the database.
            with sqlite3.connect("./database/clinicDatabase.db") as db:
                cur = db.cursor()
            insert = (
                "INSERT INTO receipt(bill_number, date, doctor_name, patient_name, patient_mobile, amount) VALUES(?,?,?,?,?,?)"
            )
            # Inserting the data into the database.
            cur.execute(insert, [patient_bill_number.get(), bill_date.get(), doctor_name.get(), patient_name.get(), patient_mobile_number.get(), bill_amount.get()])
            db.commit()

            # Disabling the entry boxes after the bill is generated.
            messagebox.showinfo("Success!!", "Bill Generated", parent=bills_ledger)
            self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.entry3.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.entry4.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")

    def clear_bill(self):
        """
        It clears the text in the text boxes and text areas.
        """
        self.fill_details_into_billWindow()
        self.entry1.configure(state="normal")
        self.entry2.configure(state="normal")
        self.entry3.configure(state="normal")
        self.entry4.configure(state="normal")
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.bill_number_msg.configure(state="normal")
        self.doctor_name_msg.configure(state="normal")
        self.patient_name_msg.configure(state="normal")
        self.patient_mobile_msg.configure(state="normal")
        self.bill_amount_msg.configure(state="normal")
        self.bill_date_msg.configure(state="normal")
        self.bill_number_msg.delete(1.0, END)
        self.doctor_name_msg.delete(1.0, END)
        self.patient_name_msg.delete(1.0, END)
        self.patient_mobile_msg.delete(1.0, END)
        self.bill_amount_msg.delete(1.0, END)
        self.bill_date_msg.delete(1.0, END)
        self.bill_number_msg.configure(state="disabled")
        self.doctor_name_msg.configure(state="disabled")
        self.patient_name_msg.configure(state="disabled")
        self.patient_mobile_msg.configure(state="disabled")
        self.bill_amount_msg.configure(state="disabled")
        self.bill_date_msg.configure(state="disabled")

    def time(self):
        """
        It takes the current time and displays it in the clock label
        """
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

page1 = LoginPage(root)
root.bind("<Return>", login)
root.mainloop()
