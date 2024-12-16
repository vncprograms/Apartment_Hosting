import tkinter as tk
from tkinter import ttk, messagebox
import re
import json
import os

# Constants for file paths (for persistent storage)
DATA_FILE = 'tenants_data.json'

def load_data():
    """Load tenant and notes data from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_data(tenants):
    """Save tenant and notes data to a JSON file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(tenants, file)

def add_tenant_to_db(first_name, last_name, apartment_number, email):
    """Simulate adding tenant to the database (for now, we log to console)."""
    print(f"Tenant Added: {first_name} {last_name}, Apartment: {apartment_number}, Email: {email}")

def add_note_to_tenant(tenant_name, apartment_number, note_type, note):
    """Simulate adding a note for a tenant (log to console)."""
    print(f"Note Added for {tenant_name} (Apartment: {apartment_number}): {note_type} - {note}")

class ApartmentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Apartment Management System")
        self.tenants = load_data()  # Load tenant data from file
        self.create_notebook()

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Create tabs
        self.create_tenants_tab()
        self.create_apartments_tab()
        self.create_revenue_tab()

    def create_tenants_tab(self):
        self.tenants_frame = ttk.Frame(self.notebook)
        self.tenants_frame.pack(fill="both", expand=True)
        self.notebook.add(self.tenants_frame, text="Tenants")

        label = tk.Label(self.tenants_frame, text="Tenant List")
        label.pack()

        self.search_label = tk.Label(self.tenants_frame, text="Search by Name or Apartment:")
        self.search_label.pack()

        self.search_entry = tk.Entry(self.tenants_frame)
        self.search_entry.pack()
        self.search_entry.bind("<KeyRelease>", self.search_tenants)

        self.tenant_listbox = tk.Listbox(self.tenants_frame, height=10, width=50)
        self.tenant_listbox.pack()

        add_tenant_button = tk.Button(self.tenants_frame, text="Add Tenant", command=self.open_add_tenant_form)
        add_tenant_button.pack()

        add_note_button = tk.Button(self.tenants_frame, text="Add Note", command=self.open_add_note_form)
        add_note_button.pack()

        self.tenant_listbox.bind("<Double-1>", self.view_tenant_details)

    def create_apartments_tab(self):
        self.apartments_frame = ttk.Frame(self.notebook)
        self.apartments_frame.pack(fill="both", expand=True)
        self.notebook.add(self.apartments_frame, text="Apartments")

        label = tk.Label(self.apartments_frame, text="Apartment List")
        label.pack()

    def create_revenue_tab(self):
        self.revenue_frame = ttk.Frame(self.notebook)
        self.revenue_frame.pack(fill="both", expand=True)
        self.notebook.add(self.revenue_frame, text="Revenue")

        label = tk.Label(self.revenue_frame, text="Revenue Information")
        label.pack()

    def open_add_tenant_form(self):
        """Open a form to add a new tenant."""
        self.add_tenant_window = tk.Toplevel(self.root)
        self.add_tenant_window.title("Add Tenant")

        tk.Label(self.add_tenant_window, text="First Name:").pack()
        self.first_name_entry = tk.Entry(self.add_tenant_window)
        self.first_name_entry.pack()

        tk.Label(self.add_tenant_window, text="Last Name:").pack()
        self.last_name_entry = tk.Entry(self.add_tenant_window)
        self.last_name_entry.pack()

        tk.Label(self.add_tenant_window, text="Apartment Number:").pack()
        self.apartment_number_entry = tk.Entry(self.add_tenant_window)
        self.apartment_number_entry.pack()

        tk.Label(self.add_tenant_window, text="Email:").pack()
        self.email_entry = tk.Entry(self.add_tenant_window)
        self.email_entry.pack()

        add_button = tk.Button(self.add_tenant_window, text="Add Tenant", command=self.add_tenant)
        add_button.pack()

    def add_tenant(self):
        """Add the tenant to the list (and ideally database)."""
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        apartment_number = self.apartment_number_entry.get()
        email = self.email_entry.get()

        if not first_name or not last_name or not apartment_number or not email:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Validate apartment number format
        if not apartment_number.isdigit():
            messagebox.showerror("Error", "Apartment number should be a number!")
            return

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        # Check if email already exists
        for tenant in self.tenants:
            if tenant['email'] == email:
                messagebox.showerror("Error", "This email is already in use!")
                return

        # Add tenant to the tenants list
        tenant = {
            'first_name': first_name,
            'last_name': last_name,
            'apartment_number': apartment_number,
            'email': email,
            'notes': []
        }
        self.tenants.append(tenant)

        self.update_tenant_listbox()

        self.add_tenant_window.destroy()

        # Save tenant data
        save_data(self.tenants)

        # Simulate adding the tenant to the database
        add_tenant_to_db(first_name, last_name, apartment_number, email)

    def search_tenants(self, event=None):
        """Search for tenants by name or apartment number."""
        search_term = self.search_entry.get().lower()

        # Filter tenants based on the search term
        filtered_tenants = [
            tenant for tenant in self.tenants
            if search_term in tenant['first_name'].lower() or
            search_term in tenant['last_name'].lower() or
            search_term in tenant['apartment_number']
        ]

        self.update_tenant_listbox(filtered_tenants)

    def update_tenant_listbox(self, tenants=None):
        """Update the tenant listbox with the current list of tenants."""
        self.tenant_listbox.delete(0, tk.END)

        tenants_to_display = tenants if tenants is not None else self.tenants

        for tenant in tenants_to_display:
            tenant_info = f"{tenant['first_name']} {tenant['last_name']} - Apartment: {tenant['apartment_number']} - Email: {tenant['email']}"
            self.tenant_listbox.insert(tk.END, tenant_info)

    def open_add_note_form(self):
        """Open a form to add a note to a tenant."""
        self.add_note_window = tk.Toplevel(self.root)
        self.add_note_window.title("Add Note")

        self.note_search_label = tk.Label(self.add_note_window, text="Search Tenant by Name or Apartment:")
        self.note_search_label.pack()

        self.note_search_entry = tk.Entry(self.add_note_window)
        self.note_search_entry.pack()
        self.note_search_entry.bind("<KeyRelease>", self.search_tenants_for_note)

        self.tenant_select_listbox = tk.Listbox(self.add_note_window, height=5, width=50)
        self.update_tenant_select_listbox()
        self.tenant_select_listbox.pack()

        self.note_type_label = tk.Label(self.add_note_window, text="Select Note Type:")
        self.note_type_label.pack()

        self.note_type_dropdown = ttk.Combobox(self.add_note_window, values=["Complaint", "Late Fee", "Maintenance Request"])
        self.note_type_dropdown.pack()

        self.note_label = tk.Label(self.add_note_window, text="Note:")
        self.note_label.pack()

        self.note_entry = tk.Entry(self.add_note_window)
        self.note_entry.pack()

        add_note_button = tk.Button(self.add_note_window, text="Add Note", command=self.add_note)
        add_note_button.pack()

    def search_tenants_for_note(self, event=None):
        """Search for tenants while adding a note."""
        search_term = self.note_search_entry.get().lower()

        filtered_tenants = [
            tenant for tenant in self.tenants
            if search_term in tenant['first_name'].lower() or
            search_term in tenant['last_name'].lower() or
            search_term in tenant['apartment_number']
        ]

        self.update_tenant_select_listbox(filtered_tenants)

    def update_tenant_select_listbox(self, tenants=None):
        """Update the tenant selection listbox in the 'Add Note' form."""
        self.tenant_select_listbox.delete(0, tk.END)

        tenants_to_display = tenants if tenants is not None else self.tenants

        for tenant in tenants_to_display:
            tenant_info = f"{tenant['first_name']} {tenant['last_name']} - Apartment: {tenant['apartment_number']}"
            self.tenant_select_listbox.insert(tk.END, tenant_info)

    def add_note(self):
        """Add a note to the selected tenant."""
        selected_tenant = self.tenant_select_listbox.curselection()
        if not selected_tenant:
            messagebox.showerror("Error", "Please select a tenant!")
            return

        tenant_info = self.tenant_select_listbox.get(selected_tenant[0])
        tenant_name, apartment_number = tenant_info.split(" - ")
        first_name, last_name = tenant_name.split(" ")

        note_type = self.note_type_dropdown.get()
        note = self.note_entry.get()

        if not note_type or not note:
            messagebox.showerror("Error", "All fields are required!")
            return

        for tenant in self.tenants:
            if tenant['first_name'] == first_name and tenant['last_name'] == last_name:
                tenant['notes'].append({'note_type': note_type, 'note': note})

        add_note_to_tenant(f"{first_name} {last_name}", apartment_number, note_type, note)

        save_data(self.tenants)  # Save the updated tenant data

        self.add_note_window.destroy()

    def view_tenant_details(self, event=None):
        """View detailed information of the selected tenant."""
        selected_tenant_index = self.tenant_listbox.curselection()
        if not selected_tenant_index:
            return

        selected_tenant = self.tenants[selected_tenant_index[0]]

        tenant_details_window = tk.Toplevel(self.root)
        tenant_details_window.title(f"Tenant Details - {selected_tenant['first_name']} {selected_tenant['last_name']}")

        details_label = tk.Label(tenant_details_window, text=f"Name: {selected_tenant['first_name']} {selected_tenant['last_name']}")
        details_label.pack()

        apartment_label = tk.Label(tenant_details_window, text=f"Apartment: {selected_tenant['apartment_number']}")
        apartment_label.pack()

        email_label = tk.Label(tenant_details_window, text=f"Email: {selected_tenant['email']}")
        email_label.pack()

        notes_label = tk.Label(tenant_details_window, text="Notes:")
        notes_label.pack()

        for note in selected_tenant['notes']:
            note_label = tk.Label(tenant_details_window, text=f"{note['note_type']}: {note['note']}")
            note_label.pack()

        edit_button = tk.Button(tenant_details_window, text="Edit Info", command=lambda: self.open_edit_tenant_form(selected_tenant))
        edit_button.pack()

    def open_edit_tenant_form(self, tenant):
        """Open a form to edit the selected tenant's information."""
        self.edit_tenant_window = tk.Toplevel(self.root)
        self.edit_tenant_window.title(f"Edit Tenant - {tenant['first_name']} {tenant['last_name']}")

        tk.Label(self.edit_tenant_window, text="First Name:").pack()
        self.edit_first_name_entry = tk.Entry(self.edit_tenant_window)
        self.edit_first_name_entry.insert(0, tenant['first_name'])
        self.edit_first_name_entry.pack()

        tk.Label(self.edit_tenant_window, text="Last Name:").pack()
        self.edit_last_name_entry = tk.Entry(self.edit_tenant_window)
        self.edit_last_name_entry.insert(0, tenant['last_name'])
        self.edit_last_name_entry.pack()

        tk.Label(self.edit_tenant_window, text="Apartment Number:").pack()
        self.edit_apartment_number_entry = tk.Entry(self.edit_tenant_window)
        self.edit_apartment_number_entry.insert(0, tenant['apartment_number'])
        self.edit_apartment_number_entry.pack()

        tk.Label(self.edit_tenant_window, text="Email:").pack()
        self.edit_email_entry = tk.Entry(self.edit_tenant_window)
        self.edit_email_entry.insert(0, tenant['email'])
        self.edit_email_entry.pack()

        save_button = tk.Button(self.edit_tenant_window, text="Save Changes", command=lambda: self.save_edited_tenant(tenant))
        save_button.pack()

    def save_edited_tenant(self, tenant):
        """Save the edited tenant information."""
        tenant['first_name'] = self.edit_first_name_entry.get()
        tenant['last_name'] = self.edit_last_name_entry.get()
        tenant['apartment_number'] = self.edit_apartment_number_entry.get()
        tenant['email'] = self.edit_email_entry.get()

        # Validate fields
        if not tenant['first_name'] or not tenant['last_name'] or not tenant['apartment_number'] or not tenant['email']:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Validate apartment number and email
        if not tenant['apartment_number'].isdigit():
            messagebox.showerror("Error", "Apartment number should be a number!")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", tenant['email']):
            messagebox.showerror("Error", "Invalid email format!")
            return

        save_data(self.tenants)  # Save the updated tenant data

        self.edit_tenant_window.destroy()
        self.update_tenant_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = ApartmentManagementApp(root)
    root.mainloop()
