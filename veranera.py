import tkinter as tk
from tkinter import ttk
import hashlib

# ---------- Principal page ----------

# Function to go to the principal page
def home():
    global text, home_frame
    home_frame = tk.Frame(window)
    home_frame.pack()
    welcome = tk.Label(home_frame, text="Welcome to",
                       font = ("Verdana", 18))
    welcome.pack()
    veranera = ttk.Label(home_frame, image=logo)
    veranera.pack()
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

# ---------- Log in ----------

# Function to log in
def signin():
    global next
    enter_email()
    next = tk.Button(account_frame, text="Next",
                     command=verify_email)
    next.pack()

# Function to verify if the email exists
def verify_email():
    global pin, pass_error
    email = the_email.get().lower()
    with open('registered_accounts.txt', 'r') as email_file:
        accounts_list = email_file.readlines()
        for line in range(0, len(accounts_list)):
            account = accounts_list[line].split()
            user = account[0]
            pin = account[1]
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
            email_error.config(text="- Email not founded",
                               fg="#FF0000")
            clean_email()

# Function to verify if the password it's corrects
def verify_password():
    password = the_pass.get()
    if password == pin:
        account_frame.pack_forget()
        menu()
    else:
        pass_error.config(text="- Incorrect password",
                          fg="#FF0000")
        the_pass.delete(0, "end")

# ---------- Sign up ----------

# Function to register an user
def signup():
    global next
    enter_email()
    next = tk.Button(account_frame, text="Next",
                     command=create_email)
    next.pack()

# Function to create an email
def create_email():
    global email, confirm_text, pass_error, confirm_pass
    email_digits = "abcdefghijklmnopqrstuvwxyz0123456789._"
    valid_domains = ["@gmail.com", "@hotmail.com", "@yahoo.com",
                    "@outlook.com", "@correounivalle.edu.co"]
    counter = 0
    try:
        email = the_email.get().lower()
        username = email[0:email.index("@")]
        domain = email[email.index("@"):len(email)]
        if len(username) == 0:
            counter = 2
        with open('registered_accounts.txt', 'r') as email_file:
            accounts_list = email_file.readlines()
            for line in range(0, len(accounts_list)):
                account = accounts_list[line].split()
                user = account[0]
                pin = account[1]
                if user == email:
                    counter = 1
                    continue
        for word in username:
            if word not in email_digits:
                counter = 2
            elif len(username) < 6 or len(username) > 30:
                counter = 2
            elif domain not in valid_domains:
                counter = 3
        if counter == 1:
            email_error.config(text="- The email already exists",
                               fg="#FF0000")
            clean_email()
        elif counter == 2:
            email_error.config(text="- Invalid username",
                               fg="#FF0000")
            clean_email()
        elif counter == 3:
            email_error.config(text="- Invalid domain",
                               fg="#FF0000")
            clean_email()
        else:
            email_error.config(text = email, fg = "#808080")
            enter_password()
            confirm_text = tk.Label(account_frame,
                                    text = "Confirm password:")
            confirm_text.pack()
            confirm_pass = tk.Entry(account_frame, width = 22,
                                    show = "*")
            confirm_pass.pack()
            pass_error = tk.Label(account_frame, text = "")
            pass_error.pack()
            register = tk.Button(account_frame, text = "Register",
                                 command = create_password)
            register.pack()
    except:
        clean_email()
        email_error.config(text = "- Error, try again",
                           fg = "#FF0000")

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
            home()
            text.config(text="- Account created succesfully!",
                        fg="#008000")
        else:
            pass_error.config(text=password_requeriments,
                              font=("Verdana", 8), fg = "#FF0000",
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

# ---------- Log out ----------
def logout():
    home()
    tab.pack_forget()

# ---------- Plates ----------

# Function to clean the plate's entrys
def clean_plate_entrys():
    name_entry.delete(0, "end")
    value_entry.delete(0, "end")
    description_entry.delete(0, "end")
    available_entry.delete(0, "end")

# Function to get the values of the plate's entrys
def plate_data():
    global name, value, description, available
    name = name_entry.get()
    value = float(value_entry.get())
    description = description_entry.get()
    available = available_entry.get().capitalize()

# Function to add a new plate in the table
def add_plate():
    available_list = ["Yes", "No"]
    try:
        plate_data()
        if len(name) == 0 or len(description) == 0:
            add_error.config(text="- There cannot be empty spaces",
                            fg="#FF0000")
            clean_plate_entrys()
        elif available not in available_list:
            add_error.config(text="- Available only gets (Yes/No)",
                            fg="#FF0000")
            clean_plate_entrys()
        else:
                # Agregar el elemento al Treeview
            plates.insert('', 'end', values=(name, value, description, available))
            clean_plate_entrys()
            add_error.config(text="")
    except:
        add_error.config(text="- Value only gets positive numbers",
                            fg="#FF0000")
        clean_plate_entrys()

# Function to update the dates of a plate
def update_plate():
    seleccion = plates.selection()
    if seleccion:
        plate_data()
        if name and value:
            plates.item(seleccion, values=(name, value, description, available))
            clean_plate_entrys()

# Function to delete a plate
def delete_plate():
    seleccion = plates.selection()
    print(plates.item(seleccion, "values")[0])
    if seleccion:
        plates.delete(seleccion)

# Function to generate the plate's table
def plates_table():
    global plates, name_entry, value_entry, description_entry, available_entry, add_error
    columns = ("Name", "Value", "Description", "Available")
    plates = ttk.Treeview(plate, columns=columns, show="headings")
    plates.column("#0", width=0, stretch=tk.NO)
    plates.column("Name", width=60, anchor=tk.CENTER)
    plates.column("Value", width=60, anchor=tk.CENTER)
    plates.column("Description", width=80)
    plates.column("Available", width=80, anchor=tk.CENTER)
    plates.heading("#0", text = "", anchor=tk.W)
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
    add_error = tk.Label(add_frame, text="")
    add_error.pack()
    add = tk.Button(add_frame, text="Add", command=add_plate)
    add.pack()
    update = tk.Button(add_frame, text="Update", command=update_plate)
    update.pack()
    delete = tk.Button(add_frame, text="Delete", command=delete_plate)
    delete.pack()

# ---------- Tables ----------
def tables():
    tree = ttk.Treeview(table)
    tree["columns"] = ("Table", "Date", "Time", "People amount")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column('Table', width=60, anchor=tk.CENTER)
    tree.column("Date", width=60, anchor=tk.CENTER)
    tree.column("Time", width=60)
    tree.column("People amount", width=100, anchor=tk.CENTER)
    tree.heading("#0", text = "", anchor=tk.W)
    tree.heading('Table', text='Table')
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("People amount", text="People amount")
    tree.pack()

# ---------- Orders ----------
def orders():
    tree = ttk.Treeview(order)
    tree["columns"] = ("Table's name", "Table's number")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Table's name", width=140, anchor=tk.CENTER)
    tree.column("Table's number", width=140, anchor=tk.CENTER)
    tree.heading("#0", text = "", anchor=tk.W)
    tree.heading("Table's name", text="Table's name")
    tree.heading("Table's number", text="Table's number")
    tree.pack()

# Function of the top menu
def menu():
    global tab, plate, table, order
    tab = ttk.Notebook(window)
    
    plate = ttk.Frame(tab)
    tab.add(plate, text="Plates")
    plates_table()
    
    table = ttk.Frame(tab)
    tab.add(table, text="Tables")
    tables()

    order = ttk.Frame(tab)
    tab.add(order, text="Orders")
    orders()

    log_out = ttk.Frame(tab)
    logout_button = tk.Button(tab, text="Log out", command=logout)
    logout_button.pack()

    tab.pack(expand=True, fil="both")

# ---------- This is where the code starts running ----------
if __name__ == '__main__':
    password_requeriments = """Must contain:
- a upper letter (A-Z)
- a lowercase letter (a-z)
- a number (0-9)
- a symbol (@*$!?\&/.-_)
- 10 characters long"""
    window = tk.Tk()
    icon = tk.PhotoImage(file="icon.png")
    logo = tk.PhotoImage(file="logo.png")
    window.iconphoto(True, icon)
    window.title("Cafetería: veranera")
    window.geometry("300x510")
    window.resizable(False, False)
    home()
    window.mainloop()