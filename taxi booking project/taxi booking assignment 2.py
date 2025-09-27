import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3

root = tk.Tk()
root.title("Taxi Booking System")

conn = sqlite3.connect('taxi_booking_system.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        name TEXT,
        email TEXT,
        phone TEXT,
        gender TEXT,
        password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ride_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        location TEXT,
        destination TEXT,
        postcode TEXT,
        date TEXT,
        time TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
''')

conn.commit()

create_account_window = None  # Define create_account_window in the global scope
username_entry = None  # Define global variables for entry fields
name_entry = None
email_entry = None
phone_entry = None
password_entry = None
gender_var = None   # global variable 
payment_var = None  # Define payment_var as a global variable





def login(username, password):
    print("Username entered:", username)  # Debugging line
    print("Password entered:", password)  # Debugging line
    
    conn = sqlite3.connect('taxi_booking_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT username, password FROM customers WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        messagebox.showinfo("Success", "Customer logged in successfully!")
        print("Logged in user:", username)  # Debugging line
        show_customer_dashboard(username)
    else:
        messagebox.showerror("Error", "Invalid credentials.")

def show_customer_dashboard(username):
    global customer_dashboard_window, message_entry
    # Get customer_id based on username
    customer_id = get_logged_in_customer_id(username)

    customer_dashboard_window = tk.Toplevel(root, bg="orange")
    customer_dashboard_window.title("Customer Dashboar")

    tk.Label(customer_dashboard_window, text="Welcome to the Customer Dashboard", bg="lightgreen", fg="black").pack()

    tk.Label(customer_dashboard_window, text="Location:", bg="lightgreen", fg="black").pack()
    location_entry = tk.Entry(customer_dashboard_window)
    location_entry.pack()

    tk.Label(customer_dashboard_window, text="Destination:", bg="lightgreen", fg="black").pack()
    destination_entry = tk.Entry(customer_dashboard_window)
    destination_entry.pack()

    tk.Label(customer_dashboard_window, text="Postcode:", bg="lightgreen", fg="black").pack()
    postcode_entry = tk.Entry(customer_dashboard_window)
    postcode_entry.pack()

    tk.Label(customer_dashboard_window, text="Date:", bg="lightgreen", fg="black").pack()
    date_entry = tk.Entry(customer_dashboard_window)
    date_entry.pack()

    tk.Label(customer_dashboard_window, text="Time:", bg="lightgreen", fg="black").pack()
    time_entry = tk.Entry(customer_dashboard_window)
    time_entry.pack()

    # payment method
    payment_method_label = tk.Label(customer_dashboard_window, text="Payment Method:", bg="lightgreen", fg="black")
    payment_method_label.pack()

    # Variable to store the payment method selected by the customer
    payment_var = tk.StringVar(value="Cash")  # Default payment method set to "Cash"

    cash_radio = tk.Radiobutton(customer_dashboard_window, text="Cash", variable=payment_var, value="Cash", bg="lightgreen", fg="black")
    cash_radio.pack()

    card_radio = tk.Radiobutton(customer_dashboard_window, text="Card", variable=payment_var, value="Card", bg="lightgreen", fg="black")
    card_radio.pack()

    request_ride_button = tk.Button(customer_dashboard_window, text="Request Ride", command=lambda: request_ride(
    location_entry.get(), destination_entry.get(), postcode_entry.get(), date_entry.get(), time_entry.get(), username), bg="lightgreen", fg="black")
    request_ride_button.pack()
     # Chat Box for Communication
    chat_box = scrolledtext.ScrolledText(customer_dashboard_window, width=40, height=10)
    chat_box.pack()

    message_label = tk.Label(customer_dashboard_window, text="Send Message to Driver", bg="lightgreen", fg="black")
    message_label.pack()

    message_entry = tk.Entry(customer_dashboard_window)
    message_entry.pack()
    
   # Send Message Button
    send_message_btn = tk.Button(customer_dashboard_window, text="Send Message", command=lambda: send_message(chat_box, message_entry.get()), bg="lightgreen", fg="black")
    send_message_btn.pack()

    view_rides_button = tk.Button(customer_dashboard_window, text="View Rides", command=lambda: view_rides(username), bg="lightgreen", fg="black")
    view_rides_button.pack()
   
    #cancel ride
    cancel_ride_button = tk.Button(customer_dashboard_window, text="Cancel Ride", command=lambda: cancel_ride(ride_id), bg="lightgreen", fg="black")
    cancel_ride_button.pack()

    # Provide Feedback and Rating
    feedback_label = tk.Label(customer_dashboard_window, text="Give Feedback:", bg="lightgreen", fg="black")
    feedback_label.pack()

    # Rating stars
    rating_frame = tk.Frame(customer_dashboard_window, bg="lightgreen")
    rating_frame.pack()

    # Create 5 stars as clickable buttons for rating
    stars = []
    for i in range(5):
        star = tk.Button(rating_frame, text="\u2605", command=lambda i=i: rate_ride(i + 1), bg="lightgreen")
        star.grid(row=0, column=i)
        stars.append(star)

    ride_id = 1  # Placeholder for ride ID (replace with the actual ride ID)

def request_ride(location, destination, postcode, date, time, username):
    conn = sqlite3.connect('taxi_booking_system.db')
    cursor = conn.cursor()

    # Get customer_id based on username
    customer_id = get_logged_in_customer_id(username)

    if customer_id:
        try:
            cursor.execute('''
                INSERT INTO ride_requests (customer_id, location, destination, postcode, date, time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (customer_id, location, destination, postcode, date, time))
            conn.commit()
            conn.close()
            messagebox.showinfo("Submitted", "Ride requested successfully!")
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Error", f"Failed to request ride: {e}")
    else:
        conn.close()
        messagebox.showerror("Error", "Customer ID not found.")

def view_rides(username):
    conn = sqlite3.connect('taxi_booking_system.db')
    cursor = conn.cursor()

    # Get customer_id based on username
    customer_id = get_logged_in_customer_id(username)

    if customer_id:
        # Get rides based on customer_id from ride_requests table
        cursor.execute("SELECT id, location, destination, date, time FROM ride_requests WHERE customer_id=?", (customer_id,))
        rides = cursor.fetchall()

        conn.close()

        if rides:
            rides_window = tk.Toplevel(root)
            rides_window.title("Your Rides")

            tk.Label(rides_window, text="Your Rides").pack()

            # Display fetched rides
            for ride in rides:
                ride_info = f"Ride ID: {ride[0]}, Location: {ride[1]}, Destination: {ride[2]}, Date: {ride[3]}, Time: {ride[4]}"
                tk.Label(rides_window, text=ride_info).pack()
        else:
            messagebox.showinfo("No Rides", "You have no previous or present rides.")
    else:
        conn.close()
        messagebox.showerror("Error", "Customer ID not found.")

def get_logged_in_customer_id(username):
    print("Username received by get_logged_in_customer_id:", username)  # Debugging line

    conn = sqlite3.connect('taxi_booking_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, username FROM customers")
    all_customers = cursor.fetchall()

    # Print all usernames present in the database
    print("Usernames in the customers table:")
    for customer in all_customers:
        print(customer[1])

    cursor.execute("SELECT id FROM customers WHERE username=?", (username,))
    customer = cursor.fetchone()

    conn.close()

    if customer:
        print("Customer ID found:", customer[0])  # Debugging line
        return customer[0]  # Returns the customer ID if found
    else:
        print("Customer ID not found")  # Debugging line
        return None  # Return None if the username is not found


def get_username_from_customer_id(customer_id):
    conn = sqlite3.connect('taxi_booking_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM customers WHERE id=?", (customer_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        username = result[0]
        return username
    else:
        return None  # Return None if the username is not found
    
def get_logged_in_username():
    # Implement this function to retrieve the currently logged-in username
    # You might use a global variable to keep track of the logged-in username
    # or retrieve it from your authentication system
    return "username"  # Replace this with the actual username if available


def cancel_ride(ride_id):
    conn = sqlite3.connect('taxi_booking_system.db')
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM ride_requests WHERE id=?", (ride_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Cancelled", "Your ride has been cancelled.")
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        messagebox.showerror("Error", f"Failed to cancel ride: {e}")
    


def rate_ride(rating):
    messagebox.showinfo("Rating", f"You rated the ride {rating} stars!")

     
def send_message(chat_box, message):
    chat_box.insert(tk.END, "Customer: " + message + "\n")
    # Simulating a reply from the driver
    chat_box.insert(tk.END, "Driver: Hello, how can I help you?\n")
    # Clear message entry field
    message_entry.delete(0, tk.END)
    
def save_account():
    username = username_entry.get() if username_entry else ""
    name = name_entry.get() if name_entry else ""
    email = email_entry.get() if email_entry else ""
    phone = phone_entry.get() if phone_entry else ""
    gender = gender_var.get() if gender_var else ""
    password = password_entry.get() if password_entry else ""

    if username and name and email and phone and gender and password:
        conn = sqlite3.connect('taxi_booking_system.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO customers (username, name, email, phone, gender, password) VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, name, email, phone, gender, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Customer account created successfully!")
            create_account_window.destroy()
        except sqlite3.IntegrityError:
            conn.close()
            messagebox.showerror("ERROR", "Username already exists.")
    else:
        messagebox.showerror("ERROR", "Please fill in all details.")
        

def show_create_account():
    global create_account_window, username_entry, email_entry, phone_entry, password_entry
    global name_entry, gender_var  # Add the global variables you're using in the function


    create_account_window = tk.Toplevel(root, bg="skyblue")
    create_account_window.title("Create Customer Account")

    tk.Label(create_account_window, text="Name: ", bg="skyblue", fg="black").pack()
    name_entry = tk.Entry(create_account_window)
    name_entry.pack()

    tk.Label(create_account_window, text="Email: ", bg="skyblue", fg="black").pack()
    email_entry = tk.Entry(create_account_window)
    email_entry.pack()

    tk.Label(create_account_window, text="Phone: ", bg="skyblue", fg="black").pack()
    phone_entry = tk.Entry(create_account_window)
    phone_entry.pack()

    tk.Label(create_account_window, text="Username: ", bg="skyblue", fg="black").pack()
    username_entry = tk.Entry(create_account_window)   # Fix: Incorrect variable name here
    username_entry.pack()

    tk.Label(create_account_window, text="Password: ", bg="skyblue", fg="black").pack()
    password_entry = tk.Entry(create_account_window, show="*")
    password_entry.pack()

    tk.Label(create_account_window, text="Gender: ", bg="skyblue", fg="black").pack()
    gender_var = tk.StringVar()
    gender_var.set("male")  # Default gender selection
    tk.Radiobutton(create_account_window, text="Male", variable=gender_var, value="male", bg="skyblue", fg="black").pack()
    tk.Radiobutton(create_account_window, text="Female", variable=gender_var, value="female", bg="skyblue", fg="black").pack()

    tk.Button(create_account_window, text="Create Account", command=save_account, bg="black", fg="skyblue").pack() 


def destroy_create_account_window():
    global create_account_window
    if create_account_window:
        create_account_window.destroy()

# Login frame
login_frame = tk.Frame(root, bg="skyblue")
login_frame.pack()

tk.Label(login_frame, text="Username:", bg="skyblue", fg="black").pack()
login_username_entry = tk.Entry(login_frame)
login_username_entry.pack()

tk.Label(login_frame, text="Password:", bg="skyblue", fg="black").pack()
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.pack()

login_button = tk.Button(login_frame, text="Login", command=lambda: login(login_username_entry.get(), login_password_entry.get()))
login_button.pack()
login_button.config(bg="black", fg="skyblue") 

create_account_button = tk.Button(login_frame, text="Create Account", command=lambda: [destroy_create_account_window(), show_create_account()])
create_account_button.pack()
create_account_button.config(bg="black", fg="skyblue") 

root.mainloop()
