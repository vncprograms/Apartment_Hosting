# Import the necessary functions from your tenant module
from app.tenant import add_notes_column, create_tenants_table

# Add the notes column to the tenants table if it doesn't exist
add_notes_column()

# Or, alternatively, you could recreate the table with the new schema if you're okay with that:
# create_tenants_table()

# Now, continue with the application logic
from app.ui import ApartmentManagementApp
import tkinter as tk

def main():
    root = tk.Tk()  # Create the Tkinter root window
    app = ApartmentManagementApp(root)  # Initialize the app with the root window
    root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    main()
