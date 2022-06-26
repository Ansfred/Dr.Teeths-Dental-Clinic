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
root.title("Welcome Admin")

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
        self.entry1.configure(font="-family {MS Reference Sans Serif} -size 18")
        # The relief style of a widget refers to certain simulated 3-D effects around the outside of the widget (Reference : https://www.tutorialspoint.com/python3/tk_relief.htm)
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)

        # Creating a text entry box and placing it on the screen.
        self.entry2 = Entry(root)
        self.entry2.place(relx=0.350, rely=0.530, width=374, height=40)
        self.entry2.configure(font="-family {MS Reference Sans Serif} -size 18")
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
                messagebox.showinfo("Login Page", "Login successful.")
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
                messagebox.showerror("Oops!!", "You are not an admin.")

        else:
            messagebox.showerror("Error!!", "Incorrect username or password.")
            page1.entry2.delete(0, END)
    
def exit():
    """
    If the user clicks the "Yes" button, the program will close. If the user clicks the "No" button, the program will not close.
    """
    exit_confirmation = messagebox.askyesno("Exit", "Are you sure you want to exit ?", parent=root)
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

def receipts():
    """
    It hides the admin window and opens the patients receipt window.
    """
    admin.withdraw()        # Hiding the admin window
    global rec
    rec = Toplevel()
    page4 = ReceiptsPage(rec)
    page4.time()
    rec.protocol("WM_DELETE_WINDOW", exit)
    rec.mainloop()


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
        self.button1.place(relx=0.02, rely=0.120, width=200, height=50)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#405763")
        self.button1.configure(cursor="hand2")      # Changing the cursor to a hand when the mouse is over the button
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#20212e")
        self.button1.configure(font="-family {Bookman Old Style} -weight {bold} -size 18")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""LOGOUT""")
        self.button1.configure(command=self.logout)

        self.button2 = Button(admin)        # Creating a button and placing it on the screen.
        self.button2.place(relx=0.2175, rely=0.708, width=180, height=63)
        self.button2.configure(relief="raised")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")      # Changing the cursor to a hand when the mouse is over the button
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Comic Sans MS} -weight {bold} -size 18")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""EMPLOYEES""")
        self.button2.configure(command=employees)

        self.button3 = Button(admin)        # Creating a button and placing it on the screen.
        self.button3.place(relx=0.665, rely=0.708, width=146, height=63)
        self.button3.configure(relief="raised")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")      # Changing the cursor to a hand when the mouse is over the button
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Comic Sans MS} -weight {bold} -size 18")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""RECEIPTS""")
        self.button3.configure(command=receipts)

    def logout(self):
        logout_confirmation = messagebox.askyesno("Logout", "Sure, you want to logout ?", parent=admin)
        if logout_confirmation == True:
            admin.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


class EmployeePage:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Employee Management")

        # Label : Tkinter Label is a widget that is used to implement display boxes where you can place text or images
        self.label1 = Label(emp)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/employee_management.png")
        self.label1.configure(image=self.img)

        self.clock = Label(emp)
        self.clock.place(relx=0.85, rely=0.0675, width=120, height=36)
        self.clock.configure(font="-family {Cambria} -size 14")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        # Creating a text box.
        self.entry1 = Entry(emp)
        self.entry1.place(relx=0.0525, rely=0.27, width=240, height=28)
        self.entry1.configure(font="-family {Cambria} -size 14")
        self.entry1.configure(relief="flat")

        # Creating a button with the text "SEARCH" and when the button is clicked, it calls the search_employee function.
        self.button1 = Button(emp)
        self.button1.place(relx=0.242, rely=0.2775, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Comic Sans MS} -weight {bold} -size 12")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""SEARCH""")
        self.button1.configure(command=self.search_employee)

        # Creating a button with the text "LOGOUT" and when the button is clicked, it calls the logout function.
        self.button2 = Button(emp)
        self.button2.place(relx=0.0375, rely=0.11, width=90, height=27.5)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#20212e")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#20212e")
        self.button2.configure(font="-family {Bookman Old Style} -weight {bold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""LOGOUT""")
        self.button2.configure(command=self.logout)

        # Creating a button with the text "ADD EMPLOYEE" and when clicked it will call the add_employee() function.
        self.button3 = Button(emp)
        self.button3.place(relx=0.065, rely=0.419, width=306, height=26)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Comic Sans MS} -weight {bold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""ADD EMPLOYEE""")
        self.button3.configure(command=self.add_employee)

        # Creating a button with the text "UPDATE EMPLOYEE" and when the button is clicked, it calls the update_employee_details function.
        self.button4 = Button(emp)
        self.button4.place(relx=0.065, rely=0.485, width=306, height=26)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Comic Sans MS} -weight {bold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""UPDATE EMPLOYEE""")
        self.button4.configure(command=self.update_employee_details)

        # Creating a button with the text "DELETE EMPLOYEE" and when the button is clicked, it calls the delete_employee function.
        self.button5 = Button(emp)
        self.button5.place(relx=0.065, rely=0.55, width=306, height=26)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#CF1E14")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#ffffff")
        self.button5.configure(background="#CF1E14")
        self.button5.configure(font="-family {Comic Sans MS} -weight {bold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""DELETE EMPLOYEE""")
        self.button5.configure(command=self.delete_employee)

        # Creating a button with the text "EXIT" and when the button is clicked, it will call the exit function.
        self.button6 = Button(emp)
        self.button6.place(relx=0.145, rely=0.8625, width=76, height=23)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#CF1E14")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#ffffff")
        self.button6.configure(background="#CF1E14")
        self.button6.configure(font="-family {Comic Sans MS} -weight {bold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""EXIT""")
        self.button6.configure(command=self.exit)

        # Creating scrollbars for the emp frame
        self.scrollbarx = Scrollbar(emp, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(emp, orient=VERTICAL)

        self.tree = ttk.Treeview(emp)       # Creating a treeview widget
        self.tree.place(relx=0.313, rely=0.190, width=875, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)       # Binding the event of selecting a treeview item to the function on_tree_select.
        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)
        self.scrollbary.place(relx=0.957, rely=0.1925, width=22, height=548)
        self.scrollbarx.place(relx=0.313, rely=0.91, width=884, height=22)

        # Configuring the columns of the treeview
        self.tree.configure(
            columns=(
                "Employee ID",
                "Employee Name",
                "Contact Number",
                "Address",
                "Aadhar Number",
                "Password",
                "Designation"
            )
        )

        # Creating a table with the given column names
        self.tree.heading("Employee ID", text="Employee ID", anchor=W)      # anchor : Used to define where text is positioned relative to a reference point
        self.tree.heading("Employee Name", text="Employee Name", anchor=W)
        self.tree.heading("Contact Number", text="Contact Number", anchor=W)
        self.tree.heading("Address", text="Address", anchor=W)
        self.tree.heading("Aadhar Number", text="Aadhar Number", anchor=W)
        self.tree.heading("Password", text="Password", anchor=W)
        self.tree.heading("Designation", text="Designation", anchor=W)

        # Setting the width of each column
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=100)
        self.tree.column("#2", stretch=NO, minwidth=0, width=180)
        self.tree.column("#3", stretch=NO, minwidth=0, width=120)
        self.tree.column("#4", stretch=NO, minwidth=0, width=150)
        self.tree.column("#5", stretch=NO, minwidth=0, width=120)
        self.tree.column("#6", stretch=NO, minwidth=0, width=90)
        self.tree.column("#7", stretch=NO, minwidth=0, width=90)

        self.display_data()

    def display_data(self):
        """
        It fetches all the data from the database and inserts it into the treeview
        """
        cur.execute("SELECT * FROM employee")
        fetched_data = cur.fetchall()
        for record in fetched_data:
            self.tree.insert("", "end", values=(record))

    def search_employee(self):
        """
        It searches for the employee ID entered in the entry box and if found, it selects the row and
        displays a messagebox.
        """
        employee_array = []
        for i in self.tree.get_children():
            employee_array.append(i)
            for j in self.tree.item(i)["values"]:
                employee_array.append(j)

        employee_to_be_searched = self.entry1.get()
        for employee in employee_array:
            if employee == employee_to_be_searched:
                self.tree.selection_set(employee_array[employee_array.index(employee_to_be_searched) - 1])
                self.tree.focus(employee_array[employee_array.index(employee_to_be_searched) - 1])
                messagebox.showinfo("Success!!", "Employee ID: {} found.".format(self.entry1.get()), parent=emp)
                break
        else: 
            messagebox.showerror("Oops!!", "Employee ID: {} not found.".format(self.entry1.get()), parent=emp)
    
    selected_items = []
    def on_tree_select(self, Event):
        """
        It clears the list of selected items, then adds the selected items to the list.
        
        :param Event: The event that triggered the function
        """
        self.selected_items.clear()
        for item in self.tree.selection():
            if item not in self.selected_items:
                self.selected_items.append(item)

    def delete_employee(self):
        """
        It deletes the selected employee(s) from the database
        """
        val_array = []
        employees_to_be_removed = []

        if len(self.selected_items) != 0:
            delete_confirmation = messagebox.askyesno("Confirm", "Are you sure you want to delete the selected employee(s)?", parent=emp)
            if delete_confirmation == True:
                for i in self.selected_items:
                    for j in self.tree.item(i)["values"]:
                        val_array.append(j)
                
                # Appending the values of the list to the employees_to_be_removed list.
                for x in range(len(val_array)):
                    if x % 7 == 0:
                        employees_to_be_removed.append(val_array[j])
                        
                flag = 1

                # Deleting the employee from the database.
                for y in employees_to_be_removed:
                    if y == "EMP0000":
                        flag = 0
                        break
                    else:
                        delete_query = "DELETE FROM employee WHERE emp_id = ?"
                        cur.execute(delete_query, [y])
                        db.commit()

                if flag == 1:
                    messagebox.showinfo("Success!!", "Employee(s) deleted from database.", parent=emp)
                    self.sel.clear()
                    self.tree.delete(*self.tree.get_children())
                    self.display_data()
                else:
                    messagebox.showerror("Error!!", "Cannot delete master admin.")
        else:
            messagebox.showerror("Error!!", "Please select an employee.", parent=emp)

    def update_employee_details(self):
        """
        It opens a new window, and inserts the values of the selected employee into the entry boxes of
        the new window.
        """
        if len(self.selected_items) == 1:
            global emp_update
            emp_update = Toplevel()
            page8 = UpdateEmployeeDetailsPage(emp_update)
            page8.time()
            
            emp_update.protocol("WM_DELETE_WINDOW", self.exit_updateEmployeePage)       # Closes the window, and calls the exit_updateEmployeePage function when the user clicks the X button.
            global val_array_2
            val_array_2 = []
            for i in self.selected_items:
                for j in self.tree.item(i)["values"]:
                    val_array_2.append(j)
            
            page8.entry1.insert(0, val_array_2[1])
            page8.entry2.insert(0, val_array_2[2])
            page8.entry5.insert(0, val_array_2[3])
            page8.entry3.insert(0, val_array_2[4])
            page8.entry6.insert(0, val_array_2[5])
            page8.entry4.insert(0, val_array_2[6])
            emp_update.mainloop()

        elif len(self.selected_items) == 0:
            messagebox.showerror("Error", "Please select an employee to update.")
        else:
            messagebox.showerror("Error", "Can only update one employee at a time.")

    def add_employee(self):
        """
        It opens a new window, and when the user clicks the X button, it closes the window and calls the exit_addEmployeePage function.
        """
        global emp_add
        emp_add = Toplevel()
        page6 = AddEmployeePage(emp_add)       # Closes the window, and calls the exit_addEmployeePage function when the user clicks the X button.
        page6.time()
        emp_add.protocol("WM_DELETE_WINDOW", self.exit_addEmployeePage)
        emp_add.mainloop()

    def exit_addEmployeePage(self):
        """
        It closes the add employee window and refreshes the main window with the new data.
        """
        emp_add.destroy()
        self.tree.delete(*self.tree.get_children())
        self.display_data()

    def exit_updateEmployeePage(self):
        """
        It closes the update employee page and refreshes the main page.
        """
        emp_update.destroy()
        self.tree.delete(*self.tree.get_children())
        self.display_data()  

    def time(self):
        """
        The function time() is called every second (1000 milliseconds) and updates the clock label with the current time
        """
        string = strftime("%H:%M:%S %p")        # strftime() : Converts a time tuple to a string according to a format specification.
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def exit(self):
        """
        If the user clicks the "Yes" button, the window is destroyed and the admin window is
        deiconified.
        """
        exit_confirmation = messagebox.askyesno("Exit", "Are you sure you want to exit ?", parent=emp)
        if exit_confirmation == True:
            emp.destroy()
            admin.deiconify()

    def logout(self):
        """
        If the user clicks yes, the employee window is destroyed and the login window is deiconified.
        """
        logout_confirmation = messagebox.askyesno("Logout", "Are you sure you want to logout ?")
        if logout_confirmation == True:
            emp.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


class AddEmployeePage:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Employee")

        self.label1 = Label(emp_add)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/add_employee.png")
        self.label1.configure(image=self.img)

        self.clock = Label(emp_add)
        self.clock.place(relx=0.84, rely=0.065, width=140, height=36)
        self.clock.configure(font="-family {Cambria} -size 14")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        # Registering the functions test_int and test_char to the emp_add event.
        self.r1 = emp_add.register(self.test_int)
        self.r2 = emp_add.register(self.test_char)

        # Creating a text box.
        self.entry1 = Entry(emp_add)
        self.entry1.place(relx=0.056, rely=0.27, width=420, height=30)
        self.entry1.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry1.configure(relief="flat")
        
        # Validating the entry2 field to only accept numbers.
        self.entry2 = Entry(emp_add)
        self.entry2.place(relx=0.056, rely=0.4325, width=420, height=30)
        self.entry2.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry2.configure(relief="flat")
        self.entry2.configure(validate="key", validatecommand=(self.r1, "%P"))

        # Validating the entry3 field to only accept numbers.
        self.entry3 = Entry(emp_add)
        self.entry3.place(relx=0.056, rely=0.6025, width=420, height=30)
        self.entry3.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r1, "%P"))

        # Validating the entry field to only accept characters.
        self.entry4 = Entry(emp_add)
        self.entry4.place(relx=0.555, rely=0.2725, width=374, height=30)
        self.entry4.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry4.configure(relief="flat")
        self.entry4.configure(validate="key", validatecommand=(self.r2, "%P"))

        # Creating a text box for the user to enter their name.
        self.entry5 = Entry(emp_add)
        self.entry5.place(relx=0.555, rely=0.435, width=374, height=30)
        self.entry5.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry5.configure(relief="flat")
        
        # Creating a text box for the user to enter their password.
        self.entry6 = Entry(emp_add)
        self.entry6.place(relx=0.555, rely=0.6025, width=374, height=30)
        self.entry6.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry6.configure(relief="flat")
        self.entry6.configure(show="*")

        # Creating a button with the text "ADD" and when the button is clicked, it will call the function "submit_new_employee_details"
        self.button1 = Button(emp_add)
        self.button1.place(relx=0.408, rely=0.836, width=110, height=38)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#20212e")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#20212e")
        self.button1.configure(font="-family {Comic Sans MS} -weight {bold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ADD""")
        self.button1.configure(command=self.submit_new_employee_details)

        # Creating a button with the text "CLEAR" and when the button is clicked, it will call the function "clear"
        self.button2 = Button(emp_add)
        self.button2.place(relx=0.526, rely=0.836, width=110, height=38)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#20212e")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#20212e")
        self.button2.configure(font="-family {Comic Sans MS} -weight {bold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clear)

    def test_int(self, val):
        """
        If the value is a digit, return True. If the value is an empty string, return True. Otherwise,
        return False
        
        :param val: The value to be tested
        :return: a boolean value.
        """
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def test_char(self, val):
        """
        If the value is a letter, return True. If the value is an empty string, return True. Otherwise,
        return False
        
        :param val: The value to be tested
        :return: True or False
        """
        if val.isalpha():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        """
        It takes the current time and displays it in the clock label
        """
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def submit_new_employee_details(self):
        """
        It takes the input from the user and checks if it is valid or not. If it is valid, it inserts
        the data into the database.
        """
        emp_name = self.entry1.get()
        emp_phone = self.entry2.get()
        emp_aadhar = self.entry3.get()
        emp_designation = self.entry4.get()
        emp_address = self.entry5.get()
        emp_password = self.entry6.get()

        if emp_name.strip():
            if is_valid_phone(emp_phone):
                if is_valid_aadhar(emp_aadhar):
                    if emp_designation:
                        if emp_address:
                            if emp_password:
                                emp_id = generate_employee_id(7)
                                insert = (
                                            "INSERT INTO employee(employee_id, name, contact_number, address, aadhar_number, password, designation) VALUES(?,?,?,?,?,?,?)"
                                        )
                                cur.execute(insert, [emp_id, emp_name, emp_phone, emp_address, emp_aadhar, emp_password, emp_designation])
                                db.commit()
                                messagebox.showinfo("Success!!", "Employee ID: {} successfully added to database.".format(emp_id), parent=emp_add)
                                self.clear()
                            else:
                                messagebox.showerror("Oops!", "Please enter a password.", parent=emp_add)
                        else:
                            messagebox.showerror("Oops!", "Please enter address.", parent=emp_add)
                    else:
                        messagebox.showerror("Oops!", "Please enter designation.", parent=emp_add)
                else:
                    messagebox.showerror("Oops!", "Invalid aadhar number.", parent=emp_add)
            else:
                messagebox.showerror("Oops!", "Invalid phone number.", parent=emp_add)
        else:
            messagebox.showerror("Oops!", "Please enter employee name.", parent=emp_add)

    def clear(self):
        """
        It deletes the contents of the entry boxes.
        """
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry5.delete(0, END)
        self.entry6.delete(0, END)


class UpdateEmployeeDetailsPage:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Update Employee")

        self.label1 = Label(emp_update)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/update_employee.png")
        self.label1.configure(image=self.img)

        self.clock = Label(emp_update)
        self.clock.place(relx=0.84, rely=0.065, width=140, height=36)
        self.clock.configure(font="-family {Cambria} -size 14")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        # Registering the functions test_int and test_char to the emp_update event.
        self.r1 = emp_update.register(self.test_int)
        self.r2 = emp_update.register(self.test_char)

        # Creating a text box.
        self.entry1 = Entry(emp_update)
        self.entry1.place(relx=0.056, rely=0.27, width=420, height=30)
        self.entry1.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry1.configure(relief="flat")
        
        # Validating the entry2 field to only accept numbers.
        self.entry2 = Entry(emp_update)
        self.entry2.place(relx=0.056, rely=0.4325, width=420, height=30)
        self.entry2.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry2.configure(relief="flat")
        self.entry2.configure(validate="key", validatecommand=(self.r1, "%P"))

        # Validating the entry3 field to only accept numbers.
        self.entry3 = Entry(emp_update)
        self.entry3.place(relx=0.056, rely=0.6025, width=420, height=30)
        self.entry3.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r1, "%P"))

        # Validating the entry field to only accept characters.
        self.entry4 = Entry(emp_update)
        self.entry4.place(relx=0.555, rely=0.2725, width=374, height=30)
        self.entry4.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry4.configure(relief="flat")
        self.entry4.configure(validate="key", validatecommand=(self.r2, "%P"))

        # Creating a text box for the user to enter their name.
        self.entry5 = Entry(emp_update)
        self.entry5.place(relx=0.555, rely=0.435, width=374, height=30)
        self.entry5.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry5.configure(relief="flat")
        
        # Creating a text box for the user to enter their password.
        self.entry6 = Entry(emp_update)
        self.entry6.place(relx=0.555, rely=0.6025, width=374, height=30)
        self.entry6.configure(font="-family {MS Reference Sans Serif} -size 15")
        self.entry6.configure(relief="flat")
        self.entry6.configure(show="*")

        # Creating a button with the text "UPDATE" and when the button is clicked, it will call the function "update_employee_details"
        self.button1 = Button(emp_update)
        self.button1.place(relx=0.408, rely=0.836, width=110, height=38)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#20212e")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#20212e")
        self.button1.configure(font="-family {Comic Sans MS} -weight {bold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""UPDATE""")
        self.button1.configure(command=self.modify_employee_details)

        # Creating a button with the text "CLEAR" and when the button is clicked, it will call the function "clear"
        self.button2 = Button(emp_update)
        self.button2.place(relx=0.526, rely=0.836, width=110, height=38)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#20212e")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#20212e")
        self.button2.configure(font="-family {Comic Sans MS} -weight {bold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clear)

    def modify_employee_details(self):
        """
        It updates the employee details in the database.
        """
        emp_name = self.entry1.get()
        emp_phone = self.entry2.get()
        emp_aadhar = self.entry3.get()
        emp_designation = self.entry4.get()
        emp_address = self.entry5.get()
        emp_password = self.entry6.get()

        if emp_name.strip():
            if is_valid_phone(emp_phone):
                if is_valid_aadhar(emp_aadhar):
                    if emp_designation:
                        if emp_address:
                            if emp_password:
                                emp_id = val_array_2[0]
                                update = (
                                            "UPDATE employee SET name = ?, contact_number = ?, address = ?, aadhar_number = ?, password = ?, designation = ? WHERE employee_id = ?"
                                        )
                                cur.execute(update, [emp_name, emp_phone, emp_address, emp_aadhar, emp_password, emp_designation, emp_id])
                                db.commit()
                                messagebox.showinfo("Success!!", "Employee ID: {} successfully updated in database.".format(emp_id), parent=emp_update)
                                val_array_2.clear()
                                page3.tree.delete(*page3.tree.get_children())
                                page3.display_data()
                                EmployeePage.selected_items.clear()
                                emp_update.destroy()
                            else:
                                messagebox.showerror("Oops!", "Please enter a password.", parent=emp_update)
                        else:
                            messagebox.showerror("Oops!", "Please enter address.", parent=emp_update)
                    else:
                        messagebox.showerror("Oops!", "Please enter designation.", parent=emp_update)
                else:
                    messagebox.showerror("Oops!", "Invalid aadhar number.", parent=emp_update)
            else:
                messagebox.showerror("Oops!", "Invalid phone number.", parent=emp_update)
        else:
            messagebox.showerror("Oops!", "Please enter employee name.", parent=emp_update)

    def clear(self):
        """
        It deletes the contents of the entry boxes.
        """
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry5.delete(0, END)
        self.entry6.delete(0, END)

    def test_int(self, val):
        """
        If the value is a digit, return True. If the value is an empty string, return True. Otherwise,
        return False
        
        :param val: The value to be tested
        :return: a boolean value.
        """
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def test_char(self, val):
        """
        If the value is a letter, return True. If the value is an empty string, return True. Otherwise, return False
        
        :param val: The value to be tested
        :return: True or False
        """
        if val.isalpha():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        """
        It takes the current time and displays it in the clock label
        """
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


class ReceiptsPage:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Receipts")

        # Label : Tkinter Label is a widget that is used to implement display boxes where you can place text or images
        self.label1 = Label(rec)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/receipts.png")
        self.label1.configure(image=self.img)

        self.clock = Label(rec)
        self.clock.place(relx=0.85, rely=0.0675, width=120, height=36)
        self.clock.configure(font="-family {Cambria} -size 14")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        # Creating a text box.
        self.entry1 = Entry(rec)
        self.entry1.place(relx=0.05375, rely=0.27, width=240, height=28)
        self.entry1.configure(font="-family {Cambria} -size 14")
        self.entry1.configure(relief="flat")

        # Creating a button with the text "SEARCH" and when the button is clicked, it calls the search_receipt function.
        self.button1 = Button(rec)
        self.button1.place(relx=0.241, rely=0.268, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Comic Sans MS} -weight {bold} -size 12")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""SEARCH""")
        self.button1.configure(command=self.search_receipt)

        # Creating a button with the text "LOGOUT" and when the button is clicked, it calls the logout function.
        self.button2 = Button(rec)
        self.button2.place(relx=0.0375, rely=0.115, width=90, height=27.5)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#20212e")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#20212e")
        self.button2.configure(font="-family {Bookman Old Style} -weight {bold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""LOGOUT""")
        self.button2.configure(command=self.logout)

        # Creating a button that will delete the receipt.
        self.button3 = Button(rec)
        self.button3.place(relx=0.065, rely=0.414, width=306, height=26)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Comic Sans MS} -weight {bold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""DELETE RECEIPT""")
        self.button3.configure(command=self.delete_receipt)

        # Creating a button with the text "EXIT" and when the button is clicked, it will call the exit function.
        self.button4 = Button(rec)
        self.button4.place(relx=0.146, rely=0.86, width=76, height=23)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Comic Sans MS} -weight {bold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""EXIT""")
        self.button4.configure(command=self.exit)

        # Creating scrollbars for the receipt frame
        self.scrollbarx = Scrollbar(rec, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(rec, orient=VERTICAL)

        self.tree = ttk.Treeview(rec)       # Creating a treeview widget.
        self.tree.place(relx=0.313, rely=0.185, width=875, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)       # Binding the event of selecting a treeview item to the function on_tree_select.
        self.tree.bind("<Double-1>", self.double_tap)       # Binding the double tap to the tree widget.

        # Configuring the scrollbars to work with the tree.
        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)
        self.scrollbary.place(relx=0.957, rely=0.1925, width=22, height=548)
        self.scrollbarx.place(relx=0.313, rely=0.91, width=884, height=22)

        # Creating a table with 6 columns.
        self.tree.configure(
            columns=(
                "Bill Number",
                "Date",
                "Doctor Name",
                "Patient Name",
                "Patient Phone Number",
                "Amount",
            )
        )
        self.tree.heading("Bill Number", text="Bill Number", anchor=W)
        self.tree.heading("Date", text="Date", anchor=W)
        self.tree.heading("Doctor Name", text="Doctor Name", anchor=W)
        self.tree.heading("Patient Name", text="Patient Name", anchor=W)
        self.tree.heading("Patient Phone Number", text="Patient Phone Number", anchor=W)
        self.tree.heading("Amount", text="Amount", anchor=W)
        
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)         # Ghost Column -> Tkinter Terminology
        self.tree.column("#1", stretch=NO, minwidth=0, width=100)
        self.tree.column("#2", stretch=NO, minwidth=0, width=100)
        self.tree.column("#3", stretch=NO, minwidth=0, width=180)
        self.tree.column("#4", stretch=NO, minwidth=0, width=180)
        self.tree.column("#5", stretch=NO, minwidth=0, width=200)
        self.tree.column("#6", stretch=NO, minwidth=0, width=110)

        self.display_data()

    def display_data(self):
        """
        It fetches all the data from the database and inserts it into the treeview.
        """
        cur.execute("SELECT * FROM receipt")
        fetched_data = cur.fetchall()
        for record in fetched_data:
            self.tree.insert("", "end", values=(record))

    selected_items = []
    def on_tree_select(self, Event):
        """
        It clears the list of selected items, then iterates through the selected items in the tree and adds them to the list of selected items.
        
        :param Event: The event that triggered the callback
        """
        self.selected_items.clear()
        for i in self.tree.selection():
            if i not in self.selected_items:
                self.selected_items.append(i)

    def double_tap(self, Event):
        """
        When the user double clicks on a row in the treeview, the function will get the value of the
        first column of the row and store it in a global variable. Then it will open a new window and
        pass the new window to a function that will populate the new window with data from the database.
        
        :param Event: The event that was triggered
        """
        item = self.tree.identify('item', Event.x, Event.y)
        global bill_num
        bill_num = self.tree.item(item)['values'][0]
        
        global bill
        bill = Toplevel()
        pg = OpenBillPage(bill)
        bill.mainloop()

    def delete_receipt(self):
        """
        It deletes the selected receipt(s) from the database
        """
        value_array = []
        to_delete = []

        if len(self.selected_items) != 0:
            delete_confirmation = messagebox.askyesno("Confirm", "Are you sure you want to delete selected receipt(s)?", parent=rec)
            if delete_confirmation == True:
                for i in self.selected_items:
                    for j in self.tree.item(i)["values"]:
                        value_array.append(j)
                
                for x in range(len(value_array)):
                    if x % 5 == 0:
                        to_delete.append(value_array[x])
                
                for y in to_delete:
                    delete = "DELETE FROM receipt WHERE bill_number = ?"
                    cur.execute(delete, [y])
                    db.commit()

                messagebox.showinfo("Success!!", "Receipt(s) deleted from database.", parent=rec)
                self.selected_items.clear()
                self.tree.delete(*self.tree.get_children())

                self.display_data()
        else:
            messagebox.showerror("Error!!", "Please select an s.", parent=rec)

    def search_receipt(self):
        """
        It searches for a bill number in the treeview and if found, it selects the row and displays a
        messagebox.
        """
        value_array = []
        for i in self.tree.get_children():
            value_array.append(i)
            for j in self.tree.item(i)["values"]:
                value_array.append(j)

        receipt_to_be_searched = self.entry1.get()
        for x in value_array:
            if x == receipt_to_be_searched:
                self.tree.selection_set(value_array[value_array.index(x) - 1])
                self.tree.focus(value_array[value_array.index(x) - 1])
                messagebox.showinfo("Success!!", "Bill Number: {} found.".format(self.entry1.get()), parent=rec)
                break
        else: 
            messagebox.showerror("Oops!!", "Bill Number: {} not found.".format(self.entry1.get()), parent=rec)

    def logout(self):
        """
        If the user clicks yes on the messagebox, the receipt window is destroyed and the login window is deiconified.
        """
        logout_confirmation = messagebox.askyesno("Logout", "Are you sure you want to logout ?")
        if logout_confirmation == True:
            rec.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)

    def time(self):
        """
        It takes the current time and displays it in the clock label
        """
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def exit(self):
        """
        If the user clicks the "Yes" button, the receipt window is destroyed and the admin window is
        deiconified
        """
        exit_confirmation = messagebox.askyesno("Exit", "Are you sure you want to exit ?", parent=rec)
        if exit_confirmation == True:
            rec.destroy()
            admin.deiconify()


class OpenBillPage:
    def __init__(self, top=None):
        top.geometry("765x488")
        top.resizable(0, 0)
        top.title("Bill")

        # Creating a label and placing it on the window.
        self.label1 = Label(bill)
        self.label1.place(relx=0, rely=0, width=765, height=488)
        self.img = PhotoImage(file="./images/bill.png")
        self.label1.configure(image=self.img)
        
        # Creating a text box in the GUI.
        self.bill_num_msg = Text(bill)
        self.bill_num_msg.place(relx=0.215, rely=0.3625, width=130, height=30)
        self.bill_num_msg.configure(font="-family {Courier} -size 11")
        self.bill_num_msg.configure(borderwidth=0)
        self.bill_num_msg.configure(background="#ffffff")

        # Creating a text box in the GUI.
        self.patient_name_msg = Text(bill)
        self.patient_name_msg.place(relx=0.685, rely=0.3625, width=130, height=30)
        self.patient_name_msg.configure(font="-family {Courier} -size 11")
        self.patient_name_msg.configure(borderwidth=0)
        self.patient_name_msg.configure(background="#ffffff")

        # Creating a text box in the GUI.
        self.doctor_name_msg = Text(bill)
        self.doctor_name_msg.place(relx=0.215, rely=0.51, width=130, height=30)
        self.doctor_name_msg.configure(font="-family {Courier} -size 11")
        self.doctor_name_msg.configure(borderwidth=0)
        self.doctor_name_msg.configure(background="#ffffff")

        # Creating a text box in the GUI.
        self.patient_phone_msg = Text(bill)
        self.patient_phone_msg.place(relx=0.79, rely=0.51, width=130, height=30)
        self.patient_phone_msg.configure(font="-family {Courier} -size 11")
        self.patient_phone_msg.configure(borderwidth=0)
        self.patient_phone_msg.configure(background="#ffffff")

        # Creating a text box in the GUI.
        self.bill_date_msg = Text(bill)
        self.bill_date_msg.place(relx=0.59, rely=0.7875, width=130, height=30)
        self.bill_date_msg.configure(font="-family {Courier} -size 11")
        self.bill_date_msg.configure(borderwidth=0)
        self.bill_date_msg.configure(background="#ffffff")

        # Creating a text box in the GUI.
        self.amount_msg = Text(bill)
        self.amount_msg.place(relx=0.61, rely=0.8775, width=130, height=30)
        self.amount_msg.configure(font="-family {Courier} -size 11")
        self.amount_msg.configure(borderwidth=0)
        self.amount_msg.configure(background="#ffffff")

        find_bill = "SELECT * FROM receipt WHERE bill_number = ?"
        cur.execute(find_bill, [bill_num])
        results = cur.fetchall()
        if results:
            self.bill_num_msg.insert(END, results[0][0])
            self.bill_num_msg.configure(state="disabled")

            self.bill_date_msg.insert(END, results[0][1])
            self.bill_date_msg.configure(state="disabled")
            
            self.doctor_name_msg.insert(END, results[0][2])
            self.doctor_name_msg.configure(state="disabled")

            self.patient_name_msg.insert(END, results[0][3])
            self.patient_name_msg.configure(state="disabled")
    
            self.patient_phone_msg.insert(END, results[0][4])
            self.patient_phone_msg.configure(state="disabled")

            self.amount_msg.insert(END, results[0][5])
            self.amount_msg.configure(state="disabled")

page1 = LoginPage(root)
root.bind("<Return>", LoginPage.login)
root.mainloop()
