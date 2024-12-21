from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QFormLayout, QLineEdit, \
    QDialogButtonBox, QListWidget, QMessageBox, QVBoxLayout, QTextEdit, QDateEdit, QComboBox
from PyQt5.QtCore import QDate
from database import load_tenants, save_tenants, update_tenant_in_db, delete_tenant_from_db, save_payment

class ApartmentManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Apartment Management App")
        self.setGeometry(100, 100, 800, 600)

        self.tenants = load_tenants()

        # Tenant List Widget
        self.tenant_list_widget = QListWidget(self)
        self.tenant_list_widget.setGeometry(50, 50, 700, 300)

        # Buttons for Add, Update, Delete, Payments, Notes
        self.add_tenant_button = QPushButton("Add Tenant", self)
        self.add_tenant_button.setGeometry(50, 370, 200, 40)
        self.add_tenant_button.clicked.connect(self.open_add_tenant_form)

        self.update_tenant_button = QPushButton("Update Tenant", self)
        self.update_tenant_button.setGeometry(300, 370, 200, 40)
        self.update_tenant_button.clicked.connect(self.open_update_tenant_form)

        self.delete_tenant_button = QPushButton("Delete Tenant", self)
        self.delete_tenant_button.setGeometry(550, 370, 200, 40)
        self.delete_tenant_button.clicked.connect(self.delete_selected_tenant)

        self.add_payment_button = QPushButton("Add Payment", self)
        self.add_payment_button.setGeometry(50, 420, 200, 40)
        self.add_payment_button.clicked.connect(self.open_add_payment_form)

        self.add_notes_button = QPushButton("Add/Edit Notes", self)
        self.add_notes_button.setGeometry(300, 420, 200, 40)
        self.add_notes_button.clicked.connect(self.open_add_notes_form)

        # Add a search bar for tenants
        self.search_input = QLineEdit(self)
        self.search_input.setGeometry(50, 470, 200, 30)
        self.search_input.setPlaceholderText("Search by name")
        self.search_input.textChanged.connect(self.search_tenants)

        self.refresh_tenant_list()

        # Styling for the UI
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border-radius: 3px;
                border: 1px solid #ccc;
            }
            QTextEdit {
                font-size: 14px;
                padding: 5px;
                border-radius: 3px;
                border: 1px solid #ccc;
            }
            QListWidget {
                font-size: 16px;
            }
        """)

    def refresh_tenant_list(self):
        self.tenant_list_widget.clear()
        for tenant in self.tenants:
            tenant_display = f"{tenant['first_name']} {tenant['last_name']} - Apt: {tenant['apartment_number']}"
            self.tenant_list_widget.addItem(tenant_display)

    def search_tenants(self):
        search_text = self.search_input.text().lower()
        filtered_tenants = [tenant for tenant in self.tenants if search_text in f"{tenant['first_name']} {tenant['last_name']}".lower()]
        self.tenant_list_widget.clear()
        for tenant in filtered_tenants:
            tenant_display = f"{tenant['first_name']} {tenant['last_name']} - Apt: {tenant['apartment_number']}"
            self.tenant_list_widget.addItem(tenant_display)

    def open_add_tenant_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Tenant")
        dialog.setGeometry(200, 200, 400, 300)

        form_layout = QFormLayout()
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.apartment_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()

        form_layout.addRow("First Name", self.first_name_input)
        form_layout.addRow("Last Name", self.last_name_input)
        form_layout.addRow("Apartment Number", self.apartment_input)
        form_layout.addRow("Email", self.email_input)
        form_layout.addRow("Phone", self.phone_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.confirm_add_tenant)
        buttons.rejected.connect(dialog.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        dialog.exec_()

    def confirm_add_tenant(self):
        new_tenant = {
            'first_name': self.first_name_input.text(),
            'last_name': self.last_name_input.text(),
            'apartment_number': self.apartment_input.text(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'notes': []
        }
        self.tenants.append(new_tenant)
        save_tenants(self.tenants)  # Save tenant list after adding the new one
        self.refresh_tenant_list()  # Refresh the list in the UI

        # Show confirmation dialog
        QMessageBox.information(self, "Tenant Added", "Tenant has been added successfully.")

    def open_update_tenant_form(self):
        selected_tenant = self.tenant_list_widget.currentItem()
        if not selected_tenant:
            QMessageBox.warning(self, "Error", "Please select a tenant to update.")
            return

        tenant_display = selected_tenant.text()
        tenant_apartment_number = tenant_display.split(" ")[-1].replace("Apt:", "").strip()

        tenant = next(tenant for tenant in self.tenants if tenant['apartment_number'] == tenant_apartment_number)

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Update Tenant {tenant['first_name']} {tenant['last_name']}")
        dialog.setGeometry(200, 200, 400, 300)

        form_layout = QFormLayout()
        self.first_name_input = QLineEdit(tenant['first_name'])
        self.last_name_input = QLineEdit(tenant['last_name'])
        self.apartment_input = QLineEdit(tenant['apartment_number'])
        self.email_input = QLineEdit(tenant['email'])
        self.phone_input = QLineEdit(tenant['phone'])

        form_layout.addRow("First Name", self.first_name_input)
        form_layout.addRow("Last Name", self.last_name_input)
        form_layout.addRow("Apartment Number", self.apartment_input)
        form_layout.addRow("Email", self.email_input)
        form_layout.addRow("Phone", self.phone_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.confirm_update_tenant(tenant))
        buttons.rejected.connect(dialog.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        dialog.exec_()

    def confirm_update_tenant(self, tenant):
        tenant['first_name'] = self.first_name_input.text()
        tenant['last_name'] = self.last_name_input.text()
        tenant['apartment_number'] = self.apartment_input.text()
        tenant['email'] = self.email_input.text()
        tenant['phone'] = self.phone_input.text()

        update_tenant_in_db(tenant)  # Save the updated tenant information
        self.refresh_tenant_list()  # Refresh the tenant list in the UI

        QMessageBox.information(self, "Tenant Updated", "Tenant information has been updated successfully.")

    def open_add_payment_form(self):
        selected_tenant = self.tenant_list_widget.currentItem()
        if not selected_tenant:
            QMessageBox.warning(self, "Error", "Please select a tenant to add a payment.")
            return

        tenant_display = selected_tenant.text()
        tenant_apartment_number = tenant_display.split(" ")[-1].replace("Apt:", "").strip()

        tenant = next(tenant for tenant in self.tenants if tenant['apartment_number'] == tenant_apartment_number)

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Add Payment for {tenant['first_name']} {tenant['last_name']}")
        dialog.setGeometry(200, 200, 400, 300)

        form_layout = QFormLayout()
        self.payment_date_input = QDateEdit(calendarPopup=True)
        self.payment_date_input.setDate(QDate.currentDate())
        self.amount_input = QLineEdit()
        self.payment_status_input = QComboBox()
        self.payment_status_input.addItems(["Paid", "Pending", "Overdue"])

        form_layout.addRow("Payment Date", self.payment_date_input)
        form_layout.addRow("Amount", self.amount_input)
        form_layout.addRow("Payment Status", self.payment_status_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.confirm_add_payment(tenant))
        buttons.rejected.connect(dialog.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        dialog.exec_()

    def confirm_add_payment(self, tenant):
        payment_date = self.payment_date_input.date().toString("yyyy-MM-dd")
        amount = float(self.amount_input.text())
        payment_status = self.payment_status_input.currentText()

        save_payment(tenant['id'], payment_date, amount, payment_status)

        QMessageBox.information(self, "Payment Added", "Payment details have been added successfully.")

    def open_add_notes_form(self):
        selected_tenant = self.tenant_list_widget.currentItem()
        if not selected_tenant:
            QMessageBox.warning(self, "Error", "Please select a tenant to add or edit notes.")
            return

        tenant_display = selected_tenant.text()
        tenant_apartment_number = tenant_display.split(" ")[-1].replace("Apt:", "").strip()

        tenant = next(tenant for tenant in self.tenants if tenant['apartment_number'] == tenant_apartment_number)

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Add/Edit Notes for {tenant['first_name']} {tenant['last_name']}")
        dialog.setGeometry(200, 200, 400, 300)

        form_layout = QFormLayout()
        self.notes_input = QTextEdit()
        self.notes_input.setText("\n".join(tenant['notes']))  # Display existing notes if available

        form_layout.addRow("Notes", self.notes_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.confirm_add_notes(tenant))
        buttons.rejected.connect(dialog.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        dialog.exec_()
    


    def confirm_add_notes(self, tenant):
        tenant['notes'] = self.notes_input.toPlainText().split("\n")  # Save notes as a list of strings
        save_tenants(self.tenants)  # Save the updated tenants list with the notes

        QMessageBox.information(self, "Notes Updated", "Tenant's notes have been updated successfully.")
    def delete_selected_tenant(self):
    # Get the selected tenant from the list
        selected_tenant = self.tenant_list_widget.currentItem()
        if not selected_tenant:
            QMessageBox.warning(self, "Error", "Please select a tenant to delete.")
        return

    # Extract apartment number or some identifier from the selected item
        tenant_display = selected_tenant.text()
        tenant_apartment_number = tenant_display.split(" ")[-1].replace("Apt:", "").strip()

        tenant = next(tenant for tenant in self.tenants if tenant['apartment_number'] == tenant_apartment_number)

    # Confirm with the user if they really want to delete
        reply = QMessageBox.question(self, 'Confirm Delete', f"Are you sure you want to delete {tenant['first_name']} {tenant['last_name']}?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.tenants.remove(tenant)
        delete_tenant_from_db(tenant)  # You can implement the function to remove tenant from the database if applicable
        save_tenants(self.tenants)  # Save the updated tenants list
        self.refresh_tenant_list()  # Refresh the tenant list in the UI
        QMessageBox.information(self, "Tenant Deleted", "Tenant has been deleted successfully.")


if __name__ == '__main__':
    app = QApplication([])
    window = ApartmentManagementApp()
    window.show()
    app.exec_()
