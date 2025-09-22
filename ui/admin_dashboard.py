import tkinter as tk
from tkinter import messagebox, ttk
from client_dashboard import ClientDashboard
from freelancer_dashboard import FreelancerDashboard
from config import connect_to_db
import hashlib

class AdminDashboard:
    def __init__(self, root, admin_id):
        self.root = root
        self.admin_id = admin_id
        self.root.title("Admin Dashboard")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ECEFF1")
        self.selected_project_id = None
        self.selected_application_id = None
        self.selected_review = None
        self.controlled_user_window = None
        self.admin_username = None
        self.admin_created_at = None

        # Styling
        self.sidebar_color = "#37474F"
        self.accent_color = "#00ACC1"
        self.bg_color = "#ffffff"
        self.text_color = "#263238"
        self.font = ("Helvetica", 11)
        self.bold_font = ("Helvetica", 12, "bold")

        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=220)
        self.sidebar.pack(side="left", fill="y")

        # Control User Section in Sidebar
        self.create_control_user_section()

        self.admin_profile_button = tk.Button(self.sidebar, text="Admin Profile", command=self.show_admin_profile_section,
                                             bg=self.sidebar_color, fg="white", relief="flat",
                                             activebackground=self.accent_color, activeforeground="white",
                                             font=self.font, pady=10)
        self.admin_profile_button.pack(fill="x", padx=10, pady=2)

        # Users Details Button in Sidebar
        self.users_details_button = tk.Button(self.sidebar, text="Users Details", command=self.show_users_details_section,
                                             bg=self.sidebar_color, fg="white", relief="flat",
                                             activebackground=self.accent_color, activeforeground="white",
                                             font=self.font, pady=10)
        self.users_details_button.pack(fill="x", padx=10, pady=2)

        # Main content frame
        self.content_frame = tk.Frame(self.root, bg=self.bg_color)
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.load_admin_data()
        self.show_welcome_message()

    def create_control_user_section(self):
        control_user_section = tk.Frame(self.sidebar, bg=self.sidebar_color)
        control_user_section.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(control_user_section, text="Control User", bg=self.sidebar_color, fg="white", font=self.bold_font).pack()
        self.user_type_var = tk.StringVar(value="")
        self.user_type_combobox = ttk.Combobox(control_user_section, textvariable=self.user_type_var,
                                               values=["client", "freelancer"], width=18)
        self.user_type_combobox.pack(pady=5)
        self.user_type_combobox.bind("<<ComboboxSelected>>", self._enable_control_button)

        self.user_id_label = tk.Label(control_user_section, text="User ID:", bg=self.sidebar_color, fg="white", font=self.font)
        self.user_id_label.pack()
        self.user_id_entry = tk.Entry(control_user_section, width=22)
        self.user_id_entry.pack(pady=5)
        self.user_id_entry.bind("<KeyRelease>", self._enable_control_button)

        self.control_button = tk.Button(control_user_section, text="Control User", command=self.show_control_user_dashboard,
                                         bg=self.accent_color, fg="white", font=self.font, relief="flat",
                                         activebackground="#00838F", activeforeground="white", state=tk.DISABLED)
        self.control_button.pack(pady=5)

    def show_users_details_section(self):
        self.clear_content()
        self.create_section_header("Users Details")

        users_frame = tk.Frame(self.content_frame, bg=self.bg_color, padx=20, pady=20)
        users_frame.pack(fill="both", expand=True)

        # Create a Canvas and Scrollbar for the users section
        self.users_canvas = tk.Canvas(users_frame, bg=self.bg_color)
        self.users_canvas.pack(side="left", fill="both", expand=True)

        self.users_scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=self.users_canvas.yview)
        self.users_scrollbar.pack(side="right", fill="y")

        self.users_canvas.configure(yscrollcommand=self.users_scrollbar.set)
        self.users_canvas.bind('<Configure>', self._on_canvas_configure)

        # Create a frame inside the Canvas to hold the user details
        self.scrollable_frame = tk.Frame(self.users_canvas, bg=self.bg_color)
        self.canvas_frame_id = self.users_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Create two columns for clients and freelancers
        columns_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        columns_frame.pack(fill="both", expand=True)

        # Left Column: Clients
        clients_frame = tk.Frame(columns_frame, bg=self.bg_color)
        clients_frame.pack(side="left", padx=20, fill="both", expand=True)

        clients_label = tk.Label(clients_frame, text="Clients", bg=self.bg_color, fg=self.text_color, font=self.bold_font)
        clients_label.pack(pady=(0, 5), anchor="w")
        self.display_clients(clients_frame)

        # Right Column: Freelancers
        freelancers_frame = tk.Frame(columns_frame, bg=self.bg_color)
        freelancers_frame.pack(side="left", padx=20, fill="both", expand=True)

        freelancers_label = tk.Label(freelancers_frame, text="Freelancers", bg=self.bg_color, fg=self.text_color, font=self.bold_font)
        freelancers_label.pack(pady=(0, 5), anchor="w")
        self.display_freelancers(freelancers_frame)

        # Update the scroll region after the content is added
        self.scrollable_frame.update_idletasks()
        self.users_canvas.configure(scrollregion=self.users_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        '''Handle the canvas configure event.'''
        self.users_canvas.configure(scrollregion=self.users_canvas.bbox("all"))
        self.users_canvas.itemconfigure(self.canvas_frame_id, width=event.width)

    def display_clients(self, parent_frame):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT client_id, name FROM clients")
            clients = cursor.fetchall()
            if clients:
                for client_id, name in clients:
                    client_info = f"Client ID: {client_id}, Name: {name}"
                    client_label = tk.Label(parent_frame, text=client_info, bg=self.bg_color, fg=self.text_color,
                                            font=self.font, anchor="w", justify="left")
                    client_label.pack(pady=2, fill="x")
            else:
                no_clients_label = tk.Label(parent_frame, text="No clients found.", bg=self.bg_color, fg="lightgray",
                                            font=self.font, anchor="w")
                no_clients_label.pack(pady=2, fill="x")
        except Exception as e:
            error_label = tk.Label(parent_frame, text=f"Error loading clients: {e}", bg=self.bg_color, fg="red",
                                    font=self.font, anchor="w")
            error_label.pack(pady=2, fill="x")
        finally:
            if conn:
                conn.close()

    def display_freelancers(self, parent_frame):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT freelancer_id, name FROM freelancers")
            freelancers = cursor.fetchall()
            if freelancers:
                for freelancer_id, name in freelancers:
                    freelancer_info = f"Freelancer ID: {freelancer_id}, Name: {name}"
                    freelancer_label = tk.Label(parent_frame, text=freelancer_info, bg=self.bg_color, fg=self.text_color,
                                                font=self.font, anchor="w", justify="left")
                    freelancer_label.pack(pady=2, fill="x")
            else:
                no_freelancers_label = tk.Label(parent_frame, text="No freelancers found.", bg=self.bg_color,
                                                fg="lightgray", font=self.font, anchor="w")
                no_freelancers_label.pack(pady=2, fill="x")
        except Exception as e:
            error_label = tk.Label(parent_frame, text=f"Error loading freelancers: {e}", bg=self.bg_color, fg="red",
                                    font=self.font, anchor="w")
            error_label.pack(pady=2, fill="x")
        finally:
            if conn:
                conn.close()

    def _enable_control_button(self, event=None):
        if self.user_type_var.get() and self.user_id_entry.get():
            self.control_button.config(state=tk.NORMAL)
        else:
            self.control_button.config(state=tk.DISABLED)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.selected_project_id = None
        self.selected_application_id = None
        self.selected_review = None

    def show_welcome_message(self):
        self.clear_content()
        welcome = tk.Label(self.content_frame, text="Welcome to Admin Dashboard",
                           font=("Helvetica", 24, "bold"), bg=self.bg_color, fg=self.text_color)
        welcome.pack(expand=True)

    def create_section_header(self, title):
        header_label = tk.Label(self.content_frame, text=title, bg=self.bg_color, fg=self.text_color,
                                font=("Helvetica", 18, "bold"), pady=20)
        header_label.pack(pady=10)

    def create_table_header(self, parent_frame, headers):
        for col, header in enumerate(headers):
            tk.Label(parent_frame, text=header, bg=self.bg_color, fg="black", font=self.bold_font, borderwidth=2,
                       relief="groove", width=18).grid(row=0, column=col, padx=5, pady=5)

    def show_admin_profile_section(self):
        self.clear_content()
        self.create_section_header("Admin Profile")

        profile_frame = tk.Frame(self.content_frame, bg=self.bg_color, padx=20, pady=20)
        profile_frame.pack(expand=True, fill="both")

        tk.Label(profile_frame, text="Username:", bg=self.bg_color, fg=self.text_color, font=self.font).grid(row=0,
                                                                                                          column=0,
                                                                                                          sticky="w",
                                                                                                          pady=5)
        username_entry = tk.Entry(profile_frame, font=self.font)
        username_entry.insert(0, self.admin_username or "")
        username_entry.grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(profile_frame, text="Created At:", bg=self.bg_color, fg=self.text_color, font=self.font).grid(row=1,
                                                                                                            column=0,
                                                                                                            sticky="w",
                                                                                                            pady=5)
        created_at_label = tk.Label(profile_frame,
                                     text=str(self.admin_created_at) if self.admin_created_at else "N/A",
                                     bg=self.bg_color, fg=self.text_color, font=self.font)
        created_at_label.grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(profile_frame, text="New Password (optional):", bg=self.bg_color, fg=self.text_color,
                   font=self.font).grid(row=2, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(profile_frame, textvariable=self.password_var, show="*", font=self.font)
        password_entry.grid(row=2, column=1, sticky="ew", pady=5)

        update_button = tk.Button(profile_frame, text="Update Profile",
                                     command=lambda: self.update_admin_profile(username_entry.get(),
                                                                             self.password_var.get()),
                                     bg=self.accent_color, fg="white", font=self.font)
        update_button.grid(row=3, column=0, columnspan=2, pady=10)
        profile_frame.columnconfigure(1, weight=1)

    def update_admin_profile(self, username, password):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            if password:
                password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
                cursor.execute("UPDATE admins SET username = %s, password_hash = %s WHERE admin_id = %s",
                               (username, password_hash, self.admin_id))
            else:
                cursor.execute("UPDATE admins SET username = %s WHERE admin_id = %s", (username, self.admin_id))

            conn.commit()
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.password_var.set("")
            self.load_admin_data()
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not update profile: {e}")
        finally:
            if conn:
                conn.close()

    def show_control_user_dashboard(self):
        user_type = self.user_type_var.get()
        user_id = self.user_id_entry.get()

        if not user_id:
            messagebox.showerror("Error", "Please enter a User ID.")
            return

        try:
            user_id = int(user_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid User ID. Must be a number.")
            return

        if self.controlled_user_window:
            self.controlled_user_window.destroy()

        self.controlled_user_window = tk.Toplevel(self.root)
        self.controlled_user_window.title(f"Controlling {user_type.capitalize()} ID: {user_id}")

        if user_type == "client":
            ClientDashboard(self.controlled_user_window, user_id)
        elif user_type == "freelancer":
            FreelancerDashboard(self.controlled_user_window, user_id)
        else:
            messagebox.showerror("Error", "Invalid User Type.")
            self.controlled_user_window.destroy()
            self.controlled_user_window = None

    def load_admin_data(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT username, created_at FROM admins WHERE admin_id = %s", (self.admin_id,))
            admin_data = cursor.fetchone()
            if admin_data:
                self.admin_username, self.admin_created_at = admin_data
            else:
                messagebox.showerror("Error", "Failed to load admin data.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading admin data: {e}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    admin_id = 1
    app = AdminDashboard(root, admin_id)
    root.mainloop()
