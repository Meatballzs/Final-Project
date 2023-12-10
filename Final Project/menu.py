import tkinter as tk
from tkinter import Entry, Button, ttk, messagebox
import traceback
import mysql.connector

def show_main_menu():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            database="db_persons",
            password=""
        )
        cursor = conn.cursor()
    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
        return

    root = tk.Tk()

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the center position
    x = (screen_width - 800) // 2
    y = (screen_height - 500) // 2

    root.geometry(f"800x500+{x}+{y}")
    root.title("Poultry Data Management System")

    def addChicken():
        add_chicken_window = tk.Toplevel()

        # Create a frame for the red border with cream background
        red_border_frame = tk.Frame(add_chicken_window, bd=2, relief='solid', highlightbackground='red', highlightcolor='red', highlightthickness=2, bg='#FFFACD')  # Cream color: #FFFACD
        red_border_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Add label at the top
        title_label = tk.Label(red_border_frame, text="Add Chicken Details", font=('Helvetica', 14, 'bold'), bg='#FFFACD', fg='red')
        title_label.grid(row=0, column=0, pady=(10, 20), columnspan=2)

        chicken_weight_label = tk.Label(red_border_frame, text="Weight (KG):", padx=10, pady=5, bg='#FFFACD')
        chicken_weight_label.grid(row=1, column=0, sticky=tk.E)

        chicken_weight_entry = Entry(red_border_frame)
        chicken_weight_entry.grid(row=1, column=1, padx=10, pady=5)

        days_label = tk.Label(red_border_frame, text="Days:", padx=10, pady=5, bg='#FFFACD')
        days_label.grid(row=2, column=0, sticky=tk.E)

        days_entry = Entry(red_border_frame)
        days_entry.grid(row=2, column=1, padx=10, pady=5)

        add_button = Button(red_border_frame, text="Add", command=lambda: addChickenDetails(chicken_weight_entry.get(), days_entry.get(), add_chicken_window))
        add_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

    def generate_next_cd_id():
        cursor.execute("SELECT MAX(CAST(SUBSTRING(id, 3) AS UNSIGNED)) FROM tb_users")
        last_cd_id_numeric = cursor.fetchone()[0]

        if last_cd_id_numeric is not None:
            next_numeric_part = last_cd_id_numeric + 1
            next_cd_id = f"CD{next_numeric_part:02}"
        else:
            next_cd_id = "CD01"

        return next_cd_id

    def addChickenDetails(chicken_weight, days, add_chicken_window):
        try:
            next_cd_id = generate_next_cd_id()

            # Use backticks around the column names with special characters
            query = "INSERT INTO tb_users (id, Days, Weight (KG)) VALUES (%s, %s, %s)"
            params = (next_cd_id, days, chicken_weight)
            cursor.execute(query, params)
            conn.commit()

        except mysql.connector.Error as e:
            print("Error executing query:", e)

        add_chicken_window.destroy()
        fetch_data()

    def fetch_data():
        try:
            cursor.execute("SELECT * FROM tb_users")
            data = cursor.fetchall()

            # Clear any previous data in the treeview
            for row in tree.get_children():
                tree.delete(row)

            # Insert the fetched data into the table
            for row in data:
                tree.insert('', 'end', values=row)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def delete_data():
        selected_item = tree.selection()
        if selected_item:
            selected_id = tree.item(selected_item, 'values')[0]
            try:
                cursor.execute("DELETE FROM tb_users WHERE id = %s", (selected_id,))
                conn.commit()

                # Remove the selected row from the treeview
                tree.delete(selected_item)

            except mysql.connector.Error as err:
                print(f"Error: {err}")

    def search_database():
        search_query = search_entry.get()

        try:
            # Check if the search query is numeric (assumed to be ID search)
            if search_query.isdigit():
                cursor.execute("SELECT * FROM tb_users WHERE id = %s", (search_query,))
            else:
                # Use backticks around the column name with special characters
                cursor.execute("SELECT * FROM tb_users WHERE id LIKE %s OR Days LIKE %s OR Weight (KG) LIKE %s", (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))

            results = cursor.fetchall()

            # Clear any previous search results in the treeview
            for row in tree.get_children():
                tree.delete(row)

            # Insert the search results into the treeview
            for row in results:
                tree.insert('', 'end', values=row)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def inventory_function():
        def add_item():
            item_name = item_name_entry.get()
            quantity = quantity_entry.get()

            if not item_name or not quantity.isdigit():
                error_label.config(text="Please enter valid data.", fg="red")
                return

            inventory_tree.insert("", "end", values=(item_name, int(quantity)))

            try:
                query = "INSERT INTO inventory (Item, Quantity) VALUES (%s, %s)"
                params = (item_name, int(quantity))
                cursor.execute(query, params)
                conn.commit()
            except mysql.connector.Error as e:
                error_label.config(text=f"Error executing query: {e}", fg="red")

            item_name_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            error_label.config(text="", fg="black")

            pass

        def delete_item():
            selected_item = inventory_tree.selection()
            if selected_item:
                selected_values = inventory_tree.item(selected_item, 'values')
                item_name, quantity = selected_values[0], selected_values[1]

                inventory_tree.delete(selected_item)

                try:
                    query = "DELETE FROM inventory WHERE Item = %s AND Quantity = %s"
                    params = (item_name, quantity)
                    cursor.execute(query, params)
                    conn.commit()
                except mysql.connector.Error as e:
                    error_label.config(text=f"Error executing query: {e}", fg="red")
            pass

        def display_items():
            try:
                cursor.execute("SELECT * FROM inventory")
                data = cursor.fetchall()

                inventory_tree.delete(*inventory_tree.get_children())

                for row in data:
                    try:
                        # Assuming column names are "Item" and "Quantity"
                        item_name = row[0] if row[0] is not None else "N/A"
                        quantity = row[1] if row[1] is not None else "N/A"
                        inventory_tree.insert('', 'end', values=(item_name, quantity))
                    except (IndexError, TypeError) as e:
                        print(f"Error inserting row {row}: {e}")

            except mysql.connector.Error as err:
                print(f"Error fetching items: {err}")
                print("Traceback:")
                traceback.print_exc()
            pass

        # Create the inventory window
        inventory_window = tk.Toplevel(root)
        inventory_window.title("Inventory")

        # Create a frame for the red border with cream background
        red_border_frame_inventory = tk.Frame(inventory_window, bd=2, relief='solid', highlightbackground='red', highlightcolor='red', highlightthickness=2, bg='#FFFACD')  # Cream color: #FFFACD
        red_border_frame_inventory.pack(expand=True, fill='both', padx=10, pady=10)

        # Update the size of the window
        inventory_window.update_idletasks()

        # Set the minimum size of the window to its current size
        inventory_window.minsize(inventory_window.winfo_width(), inventory_window.winfo_height())

        # Add widgets and configure the inventory window
        inventory_label = tk.Label(red_border_frame_inventory, text="Inventory", font=('Helvetica', 14, 'bold'))
        inventory_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Create a Treeview widget
        inventory_tree = ttk.Treeview(red_border_frame_inventory, columns=["Item", "Quantity"], show="headings")
        inventory_tree.heading("#1", text="Item")
        inventory_tree.heading("#2", text="Quantity")
        inventory_tree.grid(row=1, column=0, pady=10, padx=10, columnspan=3)

        # Entry and Label for Item
        item_name_label = tk.Label(red_border_frame_inventory, text="Item:", padx=10, pady=5)
        item_name_label.grid(row=2, column=0)
        item_name_entry = Entry(red_border_frame_inventory)
        item_name_entry.grid(row=2, column=1, pady=5)

        # Entry and Label for Quantity
        quantity_label = tk.Label(red_border_frame_inventory, text="Quantity:", padx=10, pady=5)
        quantity_label.grid(row=3, column=0)
        quantity_entry = Entry(red_border_frame_inventory)
        quantity_entry.grid(row=3, column=1, pady=5)

        # Add Item Button
        add_item_button = Button(red_border_frame_inventory, text="Add Item", command=lambda: add_item())
        add_item_button.grid(row=4, column=0, pady=10)

        # Delete Item Button
        delete_item_button = Button(red_border_frame_inventory, text="Delete Item", command=lambda: delete_item())
        delete_item_button.grid(row=4, column=1, pady=10)

        # Display Items Button
        display_items_button = Button(red_border_frame_inventory, text="Display Items", command=lambda: display_items())
        display_items_button.grid(row=4, column=2, pady=10)

        # Error Label
        error_label = tk.Label(red_border_frame_inventory, text="", fg="black")
        error_label.grid(row=5, column=0, columnspan=3, pady=10)

    def log_out():
        # Prompt the user to confirm logout
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            root.destroy()  # Close the current window (main menu)
            import login_window  # Import login_window.py
            login_window.main_screen()  # Call the main_screen function to show the login window
            

        # Create a frame for the red border with cream background
    red_border_frame = tk.Frame(root, bd=2, relief='solid', highlightbackground='red', highlightcolor='red', highlightthickness=2, bg='#FFFACD')  # Cream color: #FFFACD
    red_border_frame.pack(expand=True, fill='both', padx=10, pady=10)

    # Add label at the top
    title_label = tk.Label(red_border_frame, text="Poultry Data Management System", font=('Helvetica', 30, 'bold'), bg='#FFFACD', fg='red')
    title_label.grid(row=0, column=0, pady=10, columnspan=3)

    # Frame for Left Side (First Name, Last Name, and Buttons)
    left_frame = tk.Frame(red_border_frame, width=400, height=600, bg='#FFFACD')
    left_frame.grid(row=1, column=0, padx=10, pady=10, rowspan=4)

    # Button to Add Chicken
    add_chicken_button = Button(left_frame, text="Add Chicken", command=addChicken)
    add_chicken_button.grid(row=0, column=0, columnspan=2, pady=10)

    # Button to Display Data
    display_button = Button(left_frame, text="Display", command=fetch_data)
    display_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Button to Delete Data
    delete_button = Button(left_frame, text="Delete", command=delete_data)
    delete_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Button to Inventory
    inventory_button = Button(left_frame, text="Inventory", command=inventory_function)
    inventory_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Entry for Search
    search_entry = Entry(red_border_frame)
    search_entry.grid(row=1, column=1, pady=10, sticky="e")

    # Button to Search Data
    search_button = Button(red_border_frame, text="Search", command=search_database)
    search_button.grid(row=1, column=2, pady=10, padx=10, sticky="e")

    # Log Out Button
    log_out_button = Button(red_border_frame, text="Log Out", command=log_out)
    log_out_button.grid(row=6, column=0, columnspan=3, pady=10)

    # Treeview on the Right Side
    tree = ttk.Treeview(red_border_frame, columns=["id", "Days", "Weight (KG)"], height=50, show="headings")
    tree.heading("#1", text="ID")
    tree.heading("#2", text="Days")
    tree.heading("#3", text="Weight (KG)")
    tree.column("id", width=200)
    tree.column("Days", width=200)
    tree.column("Weight (KG)", width=200)
    tree.grid(row=2, column=1, padx=10, pady=10, columnspan=2, rowspan=3)

    # Center the Treeview in the middle
    red_border_frame.grid_rowconfigure(2, weight=1)
    red_border_frame.grid_columnconfigure(1, weight=1)

    root.mainloop()


show_main_menu