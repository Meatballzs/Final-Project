import mysql.connector
from tkinter import *
from tkinter import messagebox

# Database Connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        database="db_persons",
        password=""
    )
    cursor = conn.cursor()

except mysql.connector.Error as e:
    messagebox.showerror("Database Connection Error", f"Error: {e}")
    exit()

def login_success():
    screen.destroy()
    # This function is called upon successful login
    import menu  # Import menu.py only when login is successful
    menu.show_main_menu()

def login():
    user = username.get()
    code = password.get()

    # Check if the entered username and password match any record in the database
    cursor.execute("SELECT * FROM login WHERE Username=%s AND Password=%s", (user, code))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login", "Login successful!")
        # Call the function to handle successful login
        login_success()
    else:
        messagebox.showerror("Login", "Invalid username or password")


def signup_page():
    signup_screen = Toplevel(screen)
    signup_screen.title("Sign Up")
    signup_screen.geometry("1280x720+150+80")
    signup_screen.configure(bg="#FFFACD")  # Set background color to cream
    signup_screen.resizable(False, False)

    lblTitleSignup = Label(signup_screen, text="Sign Up", font=("arial", 50, 'bold'), fg="black", bg="#FFFACD")
    lblTitleSignup.pack(pady=50)

    bordercolor = Frame(signup_screen, bg="black", width=800, height=400)
    bordercolor.pack()

    signup_mainframe = Frame(bordercolor, bg="#FFFACD", width=800, height=400)  # Set background color to cream
    signup_mainframe.pack(padx=20, pady=20)

    Label(signup_mainframe, text="Username", font=("arial", 30, "bold"), bg="#FFFACD").place(x=100, y=150)
    Label(signup_mainframe, text="Password", font=("arial", 30, "bold"), bg="#FFFACD").place(x=100, y=250)

    signup_username = StringVar()
    signup_password = StringVar()

    entry_signup_username = Entry(signup_mainframe, textvariable=signup_username, width=12, bd=2, font=("arial", 30))
    entry_signup_username.place(x=400, y=150)
    entry_signup_password = Entry(signup_mainframe, textvariable=signup_password, width=12, bd=2, font=("arial", 30), show="*")
    entry_signup_password.place(x=400, y=250)

    def reset_signup():
        entry_signup_username.delete(0, END)
        entry_signup_password.delete(0, END)

    def signup_action():
        # Get the values from entry widgets
        new_username = signup_username.get()
        new_password = signup_password.get()

        # Insert the data into the database
        cursor.execute("INSERT INTO login (Username, Password) VALUES (%s, %s)", (new_username, new_password))
        conn.commit()

        # Display a success message
        messagebox.showinfo("Sign Up", "User signed up successfully!")

        # Reset the entry widgets
        reset_signup()

    Button(signup_mainframe, text="Sign Up", height="2", width=23, bg="#FFFF00", fg="black", bd=2, relief="raised", command=signup_action).place(x=100, y=350)
    Button(signup_mainframe, text="Reset", height="2", width=23, bg="#1089ff", fg="white", bd=2, relief="raised", command=reset_signup).place(x=300, y=350)
    Button(signup_mainframe, text="Exit", height="2", width=23, bg="#00bd56", fg="white", bd=2, relief="raised", command=signup_screen.destroy).place(x=500, y=350)


def main_screen():
    global screen
    global username
    global password

    screen = Tk()
    screen.title("Login")

    # Set the width and height of the window
    window_width = 1280
    window_height = 720

    # Get the screen width and height
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()

    # Calculate the x and y coordinates for the window to be centered
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2

    # Set the window's geometry
    screen.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    screen.configure(bg='#FFFACD')  # Set background color to cream
    screen.resizable(False, False)

    lblTitle = Label(text="Login", font=("arial", 50, 'bold'), fg="black", bg='#FFFACD')  # Set background color to cream
    lblTitle.pack(pady=50)

    bordercolor = Frame(screen, bg="black", width=800, height=400)
    bordercolor.pack()

    mainframe = Frame(bordercolor, bg="lightgray", width=800, height=400)
    mainframe.pack(padx=20, pady=20)

    Label(mainframe, text="Username", font=("arial", 30, "bold"), bg="lightgray").place(x=100, y=50)
    Label(mainframe, text="Password", font=("arial", 30, "bold"), bg="lightgray").place(x=100, y=150)

    username = StringVar()
    password = StringVar()

    entry_username = Entry(mainframe, textvariable=username, width=12, bd=2, font=("arial", 30))
    entry_username.place(x=400, y=50)
    entry_password = Entry(mainframe, textvariable=password, width=12, bd=2, font=("arial", 30), show="*")
    entry_password.place(x=400, y=150)

    def reset():
        entry_username.delete(0, END)
        entry_password.delete(0, END)

    Button(mainframe, text="Login", height="2", width=23, bg="#ed3833", fg="white", bd=2, relief="raised", command=login).place(x=100, y=250)
    Button(mainframe, text="Reset", height="2", width=23, bg="#1089ff", fg="white", bd=2, relief="raised", command=reset).place(x=300, y=250)
    Button(mainframe, text="Exit", height="2", width=23, bg="#00bd56", fg="white", bd=2, relief="raised", command=screen.destroy).place(x=500, y=250)
    Button(mainframe, text="Sign Up", height="2", width=23, bg="#FFFF00", fg="black", bd=2, relief="raised", command=signup_page).place(x=300, y=300)

    screen.mainloop()

if __name__ == "_main_":
    main_screen()