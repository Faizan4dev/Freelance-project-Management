import tkinter as tk
from tkinter import messagebox
from config import connect_to_db
import hashlib
from admin_dashboard import AdminDashboard  # Import the AdminDashboard class

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def attempt_login(name, password, role, parent_window=None):
    def debug_log(*args):
        print("[DEBUG]", *args)

    if role == "admin":
        table = "admins"
        fields = ("username", "password_hash", "admin_id")
        id_field = "admin_id"
    elif role in ["client", "freelancer"]:
        table = "clients" if role == "client" else "freelancers"
        fields = ("name", "password_hash", f"{role}_id")
        id_field = f"{role}_id"
    else:
        messagebox.showerror("Login Error", "❌ Invalid role selected.")
        return False

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = f"SELECT {fields[0]}, {fields[1]}, {fields[2]} FROM {table} WHERE {fields[0]} = %s"
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            debug_log("DB Result:", result)
        except Exception as e:
            messagebox.showerror("Query Error", f"❌ Failed to execute query.\n{str(e)}")
            cursor.close()
            conn.close()
            return False
        cursor.close()
        conn.close()

        if result:
            db_username, db_hashed_password, user_id = result
            input_hashed_password = hash_password(password)
            debug_log("Input password:", password)
            debug_log("Hashed input password:", input_hashed_password)
            debug_log("Stored password hash:", db_hashed_password)

            if input_hashed_password == db_hashed_password:
                messagebox.showinfo("Login", f"✅ Login successful as {role.capitalize()}!")

                if role == "admin":
                    from admin_dashboard import AdminDashboard
                    AdminDashboard(tk.Toplevel(parent_window), user_id)
                elif role == "client":
                    from client_dashboard import ClientDashboard
                    ClientDashboard(tk.Toplevel(parent_window), user_id)
                else:
                    from freelancer_dashboard import FreelancerDashboard
                    FreelancerDashboard(tk.Toplevel(parent_window), user_id)

                return True
            else:
                messagebox.showerror("Login Failed", "❌ Incorrect password.")
        else:
            messagebox.showerror("Login Failed", f"❌ {role.capitalize()} not found.")
    else:
        messagebox.showerror("Database Error", "❌ Failed to connect to the database.")

    return False


class AdminLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.geometry("300x200")
        self.root.configure(bg="#f0f0f0")

        self.username_label = tk.Label(root, text="Username:", bg="#f0f0f0")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(root, text="Password:", bg="#f0f0f0")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(root, text="Login", command=self._on_login, bg="#4CAF50", fg="white")
        self.login_button.pack(pady=10)

    def _on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        attempt_login(username, password, "admin", self.root)

if __name__ == "__main__":
    root = tk.Tk()
    login_window = AdminLogin(root)
    root.mainloop()