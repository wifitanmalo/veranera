import tkinter as tk
from tkinter import ttk
import hashlib
from datetime import datetime
import random


# -------------------- Principal page --------------------

# Function to go to the principal page
def home():
    global text, home_frame
    home_frame = tk.Frame(window)
    home_frame.pack()
    try:
        back_frame.pack_forget()
        account_frame.pack_forget()
        tab.pack_forget()
    except:
        print("- Start error")
    finally:
        message = tk.Label(home_frame,
                       font=("Verdana", 9),
                       justify="center",
                       text="""
In Veranera we pride ourselves on offering
a unique experience that combines delicious
flavors, a cozy atmosphere and a variety of 
services to satisfy your tastes and needs.
Come and discover the charm of Veranera
where every sip tells a story and every bite
is a delicious adventure!
""")
        message.pack()
        sign_in = tk.Button(home_frame, text="Sign in", command=signin)
        sign_in.pack()
        sign_up = tk.Button(home_frame, text="Sign up", command=signup)
        sign_up.pack()
        text = tk.Label(home_frame, text="", font=("Verdana", 10))
        text.pack()

# Function to enter the email
def enter_email():
    global the_email, email_error, email_text, account_frame
    home_frame.pack_forget() # Deletes the home elements
    account_frame = tk.Frame(window)
    account_frame.pack()
    email_text = tk.Label(account_frame, text="Email:")
    email_text.pack()
    the_email = tk.Entry(account_frame, width=22)
    the_email.pack()
    email_error = tk.Label(account_frame, text="")
    email_error.pack()

# Function to delete the text of the email
def clean_email():
    the_email.delete(0, "end")

# Function to show the password entry
def enter_password():
    global pass_text, the_pass, pass_error
    next.pack_forget()
    the_email.pack_forget()
    pass_text = tk.Label(account_frame, text="Password:")
    pass_text.pack()
    the_pass = tk.Entry(account_frame, width=22, show="*")
    the_pass.pack()

# Function to delete text of the password
def clean_pass():
    the_pass.delete(0, "end")
    confirm_pass.delete(0, "end")


# -------------------- Log in --------------------

# Function to log in
def signin():
    global next
    back.pack()
    enter_email()
    next = tk.Button(account_frame, text="Next",
                         command=verify_email)
    next.pack()
    back_frame.pack()

# Function to verify if the email exists
def verify_email():
    global pin, pass_error
    email = the_email.get().lower()
    try:
        with open('registered_accounts.txt', 'r', encoding="utf-8") as email_file:
            accounts_list = email_file.readlines()
            for line in range(0, len(accounts_list)):
                account = accounts_list[line].split()
                user = account[0]
                pin = account[2]
                if user == email:
                    email_error.config(text=email, fg="#808080")
                    enter_password()
                    pass_error = tk.Label(account_frame, text="")
                    pass_error.pack()
                    log_in = tk.Button(account_frame, text="Log in",
                                    command=verify_password)
                    log_in.pack()
                    break
            if user != email:
                email_error.config(text="- Email not found",
                                fg="#FF0000")
                clean_email()
    except FileNotFoundError:
        email_error.config(text="- Unknown error",
                                fg="#FF0000")
        clean_email()

# Function to verify if the password it's correct
def verify_password():
    password = the_pass.get()
    hash = hashlib.sha256(password.encode("utf-8"))
    print(hash.hexdigest(), pin)
    if hash.hexdigest() == pin:
        account_frame.pack_forget()
        back_frame.pack_forget()
        tab.pack(expand=True, fil="both")
    else:
        pass_error.config(text="- Incorrect password",
                          fg="#FF0000")
        the_pass.delete(0, "end")


# -------------------- Sign up --------------------

# Function to register an user
def signup():
    global next
    back.pack()
    enter_email()
    next = tk.Button(account_frame, text="Next",
                    command=create_email)
    next.pack()
    back_frame.pack()

# Function to create an email
def create_email():
    global email, confirm_text, pass_error, confirm_pass
    email_digits = "abcdefghijklmnopqrstuvwxyz0123456789._"
    valid_domains = ["@gmail.com", "@hotmail.com", "@yahoo.com",
                    "@outlook.es", "@correounivalle.edu.co"]
    try:
        email = the_email.get().lower()
        user = email[0:email.index("@")]
        domain = email[email.index("@"):len(email)]
        if len(user) == 0 or len(user) < 6 or len(user) > 30:
            raise ValueError
        elif domain not in valid_domains:
            raise Exception
        for word in user:
            if word not in email_digits:
                raise ValueError
        with open('registered_accounts.txt', 'r') as email_file:
            accounts_list = email_file.readlines()
            for line in range(0, len(accounts_list)):
                account = accounts_list[line].split()
                if account[0] == email:
                    raise KeyboardInterrupt
        email_error.config(text=email, fg="#808080")
        enter_password()
        confirm_text = tk.Label(account_frame,
                                text="Confirm password:")
        confirm_text.pack()
        confirm_pass = tk.Entry(account_frame, width = 22,
                                show="*")
        confirm_pass.pack()
        pass_error = tk.Label(account_frame, text="")
        pass_error.pack()
        register = tk.Button(account_frame, text="Register",
                            command=create_password)
        register.pack() 
    except ValueError:
        email_error.config(text="- Invalid username",
                                fg="#FF0000")
        clean_email()
    except FileNotFoundError:
        email_error.config(text="- Unknown error",
                                fg="#FF0000")
        clean_email()
    except KeyboardInterrupt:
        email_error.config(text="- Email already exists",
                                fg="#FF0000")
        clean_email()
    except:
        email_error.config(text = "- Invalid email",
                           fg = "#FF0000")
        clean_email()

# Function to create a password
def create_password():
    global password
    password = the_pass.get()
    confirm = confirm_pass.get()
    if password == confirm:
        if password_strength():
            hash = hashlib.sha256(password.encode("utf-8"))
            with open('registered_accounts.txt', 'a', encoding="utf-8") as file:
                file.write(f"{email} {password} {hash.hexdigest()}\n")
            account_frame.pack_forget()
            back_frame.pack_forget()
            home()
            text.config(text="- Account created succesfully!",
                        fg="#008000")
        else:
            pass_error.config(text="""Must contain:
- a lowercase letter (a-z)
- a upper letter (A-Z)
- a number (0-9)
- a symbol (@*$!?\&/.-_)
- 10 characters long""", font=("Verdana", 8), fg = "#FF0000",
                              justify="left")
            clean_pass()
    else:
        pass_error.config(text="- Passwords don't match",
                          fg="#FF0000")
        clean_pass()

# Function to verify the strenght of the password
def password_strength():
    low = False
    up = False
    simbol = False
    number = False
    for caracter in password:
        if caracter.islower():
            low = True
        elif caracter.isupper():
            up = True
        elif caracter.isdigit():
            number = True
        elif caracter in "@*$!?\&/.-_":
            simbol = True
    return low and up and number and simbol and len(password) >= 10


# -------------------- Menu --------------------

# Function to generate the top menu
def menu():
    global tab, plate, table, order
    tab = ttk.Notebook(window)
    plate = ttk.Frame(tab)
    tab.add(plate, text="Plates")
    plates_table()
    table = ttk.Frame(tab)
    tab.add(table, text="Tables")
    tables_data()
    order = ttk.Frame(tab)
    tab.add(order, text="Orders")
    orders_table()
    log_out = ttk.Frame(tab)
    logout_button = tk.Button(tab, text="Log out", command=home)
    logout_button.pack()


# -------------------- Plates --------------------

# Function to get the values of the plate's entrys
def plate_data():
    global name, value, description, available
    name = name_entry.get()
    value = float(value_entry.get())
    description = description_entry.get()
    available = available_entry.get().capitalize()

# Function to clean the plate's entrys
def clean_plate_entrys():
    name_entry.delete(0, "end")
    value_entry.delete(0, "end")
    description_entry.delete(0, "end")
    available_entry.delete(0, "end")

# Function to add a new plate in the table
def add_plate():
    try:
        plate_data()
        for item in plates.get_children():
            if plates.item(item, "values")[0] == name:
                raise KeyboardInterrupt
        if len(name) == 0 or len(description) == 0:
            error_text1.config(text="- There can't be empty spaces",
                            fg="#FF0000")
            clean_plate_entrys()
        elif value < 1:
            error_text1.config(text="- Negative numbers not allowed",
                            fg="#FF0000")
            clean_plate_entrys()
        elif available != "Yes" or available != "No":
            error_text1.config(text="- Available only gets (Yes/No)",
                            fg="#FF0000")
            clean_plate_entrys()
        else:
            if available == "Yes":
                available_plates.append(name)
            plates.insert('', 'end', values=(name, f"${value}", description, available))
            error_text1.config(text="- Plate added succesfully",
                               fg="#008000")
            clean_plate_entrys()
    except KeyboardInterrupt:
        error_text1.config(text="- Plate's name already exists",
                            fg="#FF0000")
        clean_plate_entrys()
    except:
        error_text1.config(text="- Error, try again",
                            fg="#FF0000")
        clean_plate_entrys()

# Function to update the dates of a plate
def update_plate():
    try:
        selection = plates.selection()
        selected_name = plates.item(selection, "values")[0]
        selection = plates.selection()
        if selection:
            plate_data()
            for item in plates.get_children():
                if item != selection[0] and plates.item(item, "values")[0] == name:
                    raise KeyboardInterrupt
            if len(name) == 0 or len(description) == 0:
                error_text1.config(text="- There can't be empty spaces",
                                fg="#FF0000")
                clean_plate_entrys()
            elif value < 1:
                error_text1.config(text="- Negative numbers not allowed",
                                fg="#FF0000")
                clean_plate_entrys()
            elif available != "Yes" or available != "No":
                error_text1.config(text="- Available only gets (Yes/No)",
                                fg="#FF0000")
                clean_plate_entrys()
            else:
                if selected_name != name:
                    if selected_name not in available_plates and available == "Yes":
                        available_plates.append(name)
                    elif selected_name in available_plates and available == "No":
                        available_plates.append(name)
                        available_plates.remove(selected_name)
                    elif selected_name in available_plates and available == "Yes":
                        available_plates.append(name)
                        available_plates.remove(selected_name)
                elif selected_name == name:
                    if name not in available_plates and available == "Yes":
                        available_plates.append(name)
                    elif name in available_plates and available == "No":
                        available_plates.remove(name)
                plates.item(selection, values=(name, f"${value}", description, available))
                error_text1.config(text="- Plate updated succesfully",
                                    fg="#008000")
                clean_plate_entrys()
    except KeyboardInterrupt:
        error_text1.config(text="- Plate's name already exists",
                            fg="#FF0000")
        clean_plate_entrys()
    except:
        error_text1.config(text="- Error, try again",
                            fg="#FF0000")
        clean_plate_entrys()          

# Function to delete a plate
def delete_plate():
    try:
        selection = plates.selection()
        delete_name = plates.item(selection, "values")[0]
        if delete_name in available_plates:
            available_plates.remove(delete_name)
        if selection:
            plates.delete(selection)
            error_text1.config(text="- Plate deleted succesfully",
                                       fg="#008000")
        clean_plate_entrys()
    except:
        error_text1.config(text="- Error, try again",
                            fg="#FF0000")
        clean_plate_entrys()

# Function to generate the plate's table
def plates_table():
    global plates, name_entry, value_entry, description_entry, available_entry, error_text1
    columns = ("Name", "Value", "Description", "Available")
    plates = ttk.Treeview(plate, columns=columns, show="headings")
    plates.column("Name", width=60, anchor=tk.CENTER)
    plates.column("Value", width=60, anchor=tk.CENTER)
    plates.column("Description", width=80)
    plates.column("Available", width=80, anchor=tk.CENTER)
    plates.heading("Name", text="Name")
    plates.heading("Value", text="Value")
    plates.heading("Description", text="Description")
    plates.heading("Available", text="Available")
    plates.pack()
    add_frame = tk.Frame(plate)
    add_frame.pack()
    name_text = tk.Label(add_frame, text="Name:")
    name_text.pack()
    name_entry = tk.Entry(add_frame)
    name_entry.pack()
    value_text = tk.Label(add_frame, text="Value:")
    value_text.pack()
    value_entry = tk.Entry(add_frame)
    value_entry.pack()
    description_box = tk.Label(add_frame, text="Description:")
    description_box.pack()
    description_entry = tk.Entry(add_frame)
    description_entry.pack()
    available_box = tk.Label(add_frame, text="Available:")
    available_box.pack()
    available_entry = tk.Entry(add_frame)
    available_entry.pack()
    error_text1 = tk.Label(add_frame, text="")
    error_text1.pack()
    add = tk.Button(add_frame, text="Add", command=add_plate)
    add.pack()
    update = tk.Button(add_frame, text="Update", command=update_plate)
    update.pack()
    delete = tk.Button(add_frame, text="Delete", command=delete_plate)
    delete.pack()


# -------------------- Tables --------------------

# Function to get the values of the table's entrys
def table_data():
    global random_table, date, hour, people, date_format, hour_format
    random_table = random.randint(1, 9)
    date = date_entry.get()
    hour = hour_entry.get()
    people = int(people_entry.get())
    date_format = datetime.strptime(date, "%d/%m/%Y")
    hour_format = datetime.strptime(hour, "%H:%M")

# Function to clean the table's entrys
def clean_table_entrys():
    date_entry.delete(0, "end")
    hour_entry.delete(0, "end")
    people_entry.delete(0, "end")

# Function to add a reservation to the table
def book_table():
    try:
        table_data()
        the_table = random_table
        for item in tables.get_children():
            if int(tables.item(item, "values")[0]) == the_table and tables.item(item, "values")[1] == date and tables.item(item, "values")[2] == hour:
                raise KeyboardInterrupt
        if people < 1:
            error_text2.config(text="- Negative numbers not allowed",
                            fg="#FF0000")
            clean_table_entrys()
        elif people > 10:
            error_text2.config(text="- People can't be more than 10",
                            fg="#FF0000")
            clean_table_entrys()
        else:
            tables.insert('', 'end', values=(the_table, date, hour, people))
            reserved_tables.append(the_table)
            error_text2.config(text="- Table reserved succesfully",
                               fg="#008000")
            clean_table_entrys()
    except ValueError:
        error_text2.config(text="- Invalid date or hour",
                            fg="#FF0000")
        clean_table_entrys()
    except KeyboardInterrupt:
        error_text2.config(text="- Table not available for that date",
                            fg="#FF0000")
        clean_table_entrys()

# Function to update the dates of a plate
def update_table():
    try:
        selection = tables.selection()
        if selection:
            table_data()
            the_table = random_table
            for item in tables.get_children():
                if item != selection[0] and int(tables.item(item, "values")[0]) == the_table and tables.item(item, 'values')[1] == date and tables.item(item, 'values')[2] == hour:
                    raise KeyboardInterrupt
            if people < 1:
                error_text2.config(text="- Negative numbers not allowed",
                                fg="#FF0000")
                clean_table_entrys()
            else:
                tables.item(selection, values=(int(tables.item(item, "values")[0]), date, hour, people))
                error_text2.config(text="- Table updated succesfully",
                                fg="#008000")
                clean_table_entrys()
    except ValueError:
        error_text2.config(text="- Invalid date or hour",
                            fg="#FF0000")
        clean_table_entrys()
    except KeyboardInterrupt:
        error_text2.config(text="- Table not available for that date",
                            fg="#FF0000")
        clean_table_entrys()

# Function to delete a table reservation
def delete_table():
    try:
        selection = tables.selection()
        selected_table = int(tables.item(selection, "values")[0])
        if selection:
            tables.delete(selection)
            reserved_tables.remove(selected_table)
            clean_table_entrys()
    except:
        error_text2.config(text="- Error, try again",
                            fg="#FF0000")
        clean_table_entrys()

# Function to generate the table's table
def tables_data():
    global tables, date_entry, hour_entry, people_entry, error_text2
    columns = ("Table", "Date", "Hour", "# of people")
    tables = ttk.Treeview(table, columns=columns, show="headings")
    tables.column("Table", width=60, anchor=tk.CENTER)
    tables.column("Date", width=80, anchor=tk.CENTER)
    tables.column("Hour", width=60)
    tables.column("# of people", width=80, anchor=tk.CENTER)
    tables.heading("Table", text="Table")
    tables.heading("Date", text="Date")
    tables.heading("Hour", text="Hour")
    tables.heading("# of people", text="# of people")
    tables.pack()
    add_frame = tk.Frame(table)
    add_frame.pack()
    date_text = tk.Label(add_frame, text="Date (DD/MM/YYYY):")
    date_text.pack()
    date_entry = tk.Entry(add_frame)
    date_entry.pack()
    hour_text = tk.Label(add_frame, text="Hour (HH:MM):")
    hour_text.pack()
    hour_entry = tk.Entry(add_frame)
    hour_entry.pack()
    people_text = tk.Label(add_frame, text="Amount of people:")
    people_text.pack()
    people_entry = tk.Entry(add_frame)
    people_entry.pack()
    error_text2 = tk.Label(add_frame, text="")
    error_text2.pack()
    add = tk.Button(add_frame, text="Add", command=book_table)
    add.pack()
    update = tk.Button(add_frame, text="Update", command=update_table)
    update.pack()
    delete = tk.Button(add_frame, text="Delete", command=delete_table)
    delete.pack()


# -------------------- Orders --------------------

# Function to get the values of the order's entrys
def order_data():
    global plate_name, table_number
    plate_name = plate_entry.get()
    table_number = int(table_entry.get())

# Function to clean the plate's entrys
def clean_order_entrys():
    plate_entry.delete(0, "end")
    table_entry.delete(0, "end")

# Function to add a new order in the table
def add_order():
    try:
        order_data()
        if len(plate_name) == 0:
            error_text3.config(text="- There can't be empty spaces",
                            fg="#FF0000")
            clean_order_entrys()
        elif plate_name not in available_plates:
            error_text3.config(text="- Plate isn't available",
                            fg="#FF0000")
            clean_order_entrys()
        elif table_number < 1:
            error_text3.config(text="- Negative numbers not allowed",
                            fg="#FF0000")
            clean_order_entrys()
        elif table_number not in reserved_tables:
            error_text3.config(text="- Table not reserved yet",
                            fg="#FF0000")
            clean_order_entrys()
        else:
            orders.insert('', 'end', values=(plate_name, table_number))
            error_text3.config(text="- Order added succesfully",
                               fg="#008000")
            clean_order_entrys()
    except:
        error_text3.config(text="- Error, try again",
                            fg="#FF0000")
        clean_order_entrys()

# Function to update the dates of a plate
def update_order():
    try:
        selection = orders.selection()
        if selection:
            order_data()
            if len(plate_name) == 0:
                error_text3.config(text="- Can't be empty spaces",
                                fg="#FF0000")
                clean_order_entrys()
            elif table_number < 1:
                error_text3.config(text="- Negative numbers not allowed",
                                fg="#FF0000")
                clean_order_entrys()
            elif plate_name not in available_plates:
                error_text3.config(text="- Plate isn't available",
                            fg="#FF0000")
                clean_order_entrys()
            else:
                orders.item(selection,
                            values=(plate_name, table_number))
                error_text3.config(text="- Order updated succesfully",
                                    fg="#008000")
                clean_order_entrys()
        else:
            error_text3.config(text="- Select an order first",
                            fg="#FF0000")
            clean_order_entrys()    
    except:
        error_text3.config(text="- Error, try again",
                            fg="#FF0000")
        clean_order_entrys()

# Function to delete a plate
def delete_order():
    selection = orders.selection()
    if selection:
        orders.delete(selection)
        error_text3.config(text="- Order deleted succesfully",
                            fg="#008000")
    else:
        error_text3.config(text="- Select an order first",
                            fg="#FF0000")
    clean_order_entrys()
    
# Function to generate the order's table
def orders_table():
    global orders, plate_entry, table_entry, error_text3
    columns = ("Plate's name:", "Table's number:")
    orders = ttk.Treeview(order, columns=columns, show="headings")
    orders.column("Plate's name:", width=140, anchor=tk.CENTER)
    orders.column("Table's number:", width=140, anchor=tk.CENTER)
    orders.heading("#0", text = "", anchor=tk.W)
    orders.heading("Plate's name:", text="Plate's name:")
    orders.heading("Table's number:", text="Table's number:")
    orders.pack()
    add_frame = tk.Frame(order)
    add_frame.pack()
    plate_text = tk.Label(add_frame, text="Plate's name:")
    plate_text.pack()
    plate_entry = tk.Entry(add_frame)
    plate_entry.pack()
    table_text = tk.Label(add_frame, text="Table's number:")
    table_text.pack()
    table_entry = tk.Entry(add_frame)
    table_entry.pack()
    error_text3 = tk.Label(add_frame, text="")
    error_text3.pack()
    add = tk.Button(add_frame, text="Add", command=add_order)
    add.pack()
    update = tk.Button(add_frame, text="Update", command=update_order)
    update.pack()
    delete = tk.Button(add_frame, text="Delete", command=delete_order)
    delete.pack()

# This is where the code starts running
if __name__ == '__main__':
    reserved_tables = []
    available_plates = []
    try:
        window = tk.Tk()
        back_frame = tk.Frame(window)
        back = tk.Button(back_frame, text="Back",
                command=home)
        back.pack()
        icon = tk.PhotoImage(file="icon.png")
        logo = tk.PhotoImage(file="logo.png")
        window.iconphoto(True, icon)
        veranera = ttk.Label(window, image=logo)
        veranera.pack()
    except:
        print("- Error loading images")
    finally:
        window.title("Coffee shop: veranera")
        window.geometry("300x550")
        window.resizable(False, False)
        home()
        menu()
        window.mainloop()