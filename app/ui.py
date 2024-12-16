import tkinter as tk
from tkinter import ttk, messagebox

# Dummy function to simulate adding a tenant or note (For database integration, replace these with actual DB code)
def add_tenant_to_db(first_name, last_name, apartment_number, email):
    print(f"Tenant Added: {first_name} {last_name}, Apartment: {apartment_number}, Email: {email}")

def add_note_to_tenant(tenant_name, apartment_number, note_type, note):
    print(f"Note Added for {tenant_name} (Apartment: {apartment_number}): {note_type} - {note}")

class ApartmentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Apartment Management System")
        self.tenants = []  # List to store tenants as dictionaries
        self.create_notebook()

    def create_notebook(self):
        # Create the notebook widget (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Create the tabs
        self.create_tenants_tab()
        self.create_apartments_tab()
        self.create_revenue_tab()

    def create_tenants_tab(self):
        self.tenants_frame = ttk.Frame(self.notebook)
        self.tenants_frame.pack(fill="both", expand=True)
        self.notebook.add(self.tenants_frame, text="Tenants")  # Add this frame as a tab

        # Add content for the Tenants tab
        label = tk.Label(self.tenants_frame, text="Tenant List")
        label.pack()

        # Search bar for tenants
        self.search_label = tk.Label(self.tenants_frame, text="Search by Name or Apartment:")
        self.search_label.pack()

        self.search_entry = tk.Entry(self.tenants_frame)
        self.search_entry.pack()
        self.search_entry.bind("<KeyRelease>", self.search_tenants)  # Trigger search as user types

        # Create a Listbox or Treeview to show the list of tenants
        self.tenant_listbox = tk.Listbox(self.tenants_frame, height=10, width=50)
        self.tenant_listbox.pack()

        # Add a button to show the "Add Tenant" form
        add_tenant_button = tk.Button(self.tenants_frame, text="Add Tenant", command=self.open_add_tenant_form)
        add_tenant_button.pack()

        # Add a button to show the "Add Note" form
        add_note_button = tk.Button(self.tenants_frame, text="Add Note", command=self.open_add_note_form)
        add_note_button.pack()

    def create_apartments_tab(self):
        self.apartments_frame = ttk.Frame(self.notebook)
        self.apartments_frame.pack(fill="both", expand=True)
        self.notebook.add(self.apartments_frame, text="Apartments")  # Add this frame as a tab

        # Add content for the Apartments tab
        label = tk.Label(self.apartments_frame, text="Apartment List")
        label.pack()

    def create_revenue_tab(self):
        self.revenue_frame = ttk.Frame(self.notebook)
        self.revenue_frame.pack(fill="both", expand=True)
        self.notebook.add(self.revenue_frame, text="Revenue")  # Add this frame as a tab

        # Add content for the Revenue tab
        label = tk.Label(self.revenue_frame, text="Revenue Information")
        label.pack()

    def open_add_tenant_form(self):
        """Open a form to add a new tenant."""
        self.add_tenant_window = tk.Toplevel(self.root)
        self.add_tenant_window.title("Add Tenant")

        # Form to add tenant details
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

        # Add tenant to the tenants list
        tenant = {
            'first_name': first_name,
            'last_name': last_name,
            'apartment_number': apartment_number,
            'email': email,
            'notes': []  # Initialize an empty list for notes
        }
        self.tenants.append(tenant)

        # Add tenant to the Listbox
        self.update_tenant_listbox()

        # Close the "Add Tenant" form
        self.add_tenant_window.destroy()

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

        # Update the tenant listbox to display filtered tenants
        self.update_tenant_listbox(filtered_tenants)

    def update_tenant_listbox(self, tenants=None):
        """Update the tenant listbox with the current list of tenants."""
        # Clear the current listbox
        self.tenant_listbox.delete(0, tk.END)

        # Use the provided tenants list or the full tenant list
        tenants_to_display = tenants if tenants is not None else self.tenants

        # Populate the listbox with tenant info
        for tenant in tenants_to_display:
            tenant_info = f"{tenant['first_name']} {tenant['last_name']} - Apartment: {tenant['apartment_number']} - Email: {tenant['email']}"
            self.tenant_listbox.insert(tk.END, tenant_info)

    def open_add_note_form(self):
        """Open a form to add a note to a tenant."""
        self.add_note_window = tk.Toplevel(self.root)
        self.add_note_window.title("Add Note")

        # Select tenant (use the Listbox to select a tenant)
        self.select_tenant_label = tk.Label(self.add_note_window, text="Select Tenant (by Name or Apartment):")
        self.select_tenant_label.pack()

        # Tenant Listbox with Names and Apartments
        self.tenant_select_listbox = tk.Listbox(self.add_note_window, height=5, width=50)
        for tenant in self.tenants:
            tenant_info = f"{tenant['first_name']} {tenant['last_name']} - Apartment: {tenant['apartment_number']}"
            self.tenant_select_listbox.insert(tk.END, tenant_info)
        self.tenant_select_listbox.pack()

        # Select note type
        self.note_type_label = tk.Label(self.add_note_window, text="Select Note Type:")
        self.note_type_label.pack()

        self.note_type_dropdown = ttk.Combobox(self.add_note_window, values=["Complaint", "Late Fee", "Maintenance Request"])
        self.note_type_dropdown.pack()

        # Enter note
        self.note_label = tk.Label(self.add_note_window, text="Note:")
        self.note_label.pack()

        self.note_entry = tk.Entry(self.add_note_window)
        self.note_entry.pack()

        # Add note button
        add_note_button = tk.Button(self.add_note_window, text="Add Note", command=self.add_note)
        add_note_button.pack()

    def add_note(self):
        """Add a note to the selected tenant."""
        selected_tenant = self.tenant_select_listbox.curselection()
        if not selected_tenant:
            messagebox.showerror("Error", "Please select a tenant!")
            return

        tenant_info = self.tenant_select_listbox.get(selected_tenant[0])
        tenant_name, apartment_number = tenant_info.split(" - ")
        first_name, last_name = tenant_name.split(" ")

        # Get note type and note text
        note_type = self.note_type_dropdown.get()
        note = self.note_entry.get()

        if not note_type or not note:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Find tenant and add the note
        for tenant in self.tenants:
            if tenant['first_name'] == first_name and tenant['last_name'] == last_name:
                tenant['notes'].append({'note_type': note_type, 'note': note})

        # Add note to the selected tenant (this is just a simulation)
        add_note_to_tenant(f"{first_name} {last_name}", apartment_number, note_type, note)

        # Close the "Add Note" form
        self.add_note_window.destroy()

def main():
    root = tk.Tk()
    app = ApartmentManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
