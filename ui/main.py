import tkinter as tk
from config import connect_to_db
from role_selection import FPMSApp
from login_window import show_login_window  # Import the login window function


if __name__ == "__main__":
    connection = connect_to_db()
    root = tk.Tk()
    app = FPMSApp(root, connection)  # Initialize the role selection
    root.mainloop()