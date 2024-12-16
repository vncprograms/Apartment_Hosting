from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget, QDialog, QFormLayout, QDialogButtonBox, QTextEdit, QDateEdit, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import sys

class ApartmentManagementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Apartment Management System")
        self.setGeometry(100, 100, 800, 600)  # Increased size for better spacing

        self.tenants = []  # List to store tenant data

        # Apply StyleSheet for aesthetics
        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit, QTextEdit {
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
            QListWidget {
                font-size: 16px;
                padding: 10px;
                background-color: #fff;
                border-radius: 5px;
                border: 1px solid #ddd;
                height: 150px;
            }
        """)

        # UI setup
        self.layout = QVBoxLayout(self)

        # Tenant List
        self.tenant_list_label = QLabel("Tenant List:")
        self.layout.addWidget(self.tenant_list_label)

        self.tenant_list_widget = QListWidget(self)
        self.layout.addWidget(self.tenant_list_widget)

        # Add Tenant Button
        self.add_tenant_button = QPushButton("Add Tenant", self)
        self.add_tenant_button.clicked.connect(self.open_add_tenant_form)
        self.layout.addWidget(self.add_tenant_button)

        # Add Note Button
        self.add_note_button = QPushButton("Add Note/Complaint/Payment", self)
        self.add_note_button.clicked.connect(self.open_add_note_form)
        self.layout.addWidget(self.add_note_button)

        # View Notes Button
        self.view_notes_button = QPushButton("View Notes/Complaints/Payments", self)
        self.view_notes_button.clicked.connect(self.view_notes)
        self.layout.addWidget(self.view_notes_button)

        # Generate Report Button
        self.report_button = QPushButton("Generate Report", self)
        self.report_button.clicked.connect(self.generate_report)
        self.layout.addWidget(self.report_button)

        # Delete Tenant Button
        self.delete_tenant_button = QPushButton("Delete Tenant", self)
        self.delete_tenant_button.clicked.connect(self.delete_tenant)
        self.layout.addWidget(self.delete_tenant_button)

        # Update Tenant Button
        self.update_tenant_button = QPushButton("Update Tenant", self)
        self.update_tenant_button.clicked.connect(self.open_update_tenant_form)
        self.layout.addWidget(self.update_tenant_button)

    def open_add_tenant_form(self):
        """Open a form to add a new tenant."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Tenant")

        form_layout = QFormLayout()

        self.first_name_input = QLineEdit(dialog)
        form_layout.addRow("First Name:", self.first_name_input)

        self.last_name_input = QLineEdit(dialog)
        form_layout.addRow("Last Name:", self.last_name_input)

        self.apartment_input = QLineEdit(dialog)
        form_layout.addRow("Apartment Number:", self.apartment_input)

        self.email_input = QLineEdit(dialog)
        form_layout.addRow("Email:", self.email_input)

        self.phone_input = QLineEdit(dialog)
        form_layout.addRow("Phone Number:", self.phone_input)

        self.payment_input = QLineEdit(dialog)
        form_layout.addRow("Payment Amount:", self.payment_input)

        self.payment_date_input = QDateEdit(dialog)
        self.payment_date_input.setDate(QDate.currentDate())
        form_layout.addRow("Payment Date:", self.payment_date_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.confirm_action(self.add_tenant, dialog))
        buttons.rejected.connect(dialog.reject)

        form_layout.addWidget(buttons)
        dialog.setLayout(form_layout)

        dialog.exec_()

    def add_tenant(self):
        """Add the tenant to the list."""
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        apartment_number = self.apartment_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        payment_amount = self.payment_input.text()
        payment_date = self.payment_date_input.date().toString(Qt.ISODate)

        if not first_name or not last_name or not apartment_number or not email or not phone:
            return  # Don't proceed if fields are empty

        # Prevent duplicates
        for tenant in self.tenants:
            if tenant['first_name'] == first_name and tenant['last_name'] == last_name and tenant['apartment_number'] == apartment_number:
                return  # Tenant already exists, no need to add again

        tenant = {
            'first_name': first_name,
            'last_name': last_name,
            'apartment_number': apartment_number,
            'email': email,
            'phone': phone,
            'notes': [],
            'complaints': [],
            'payments': [{'amount': payment_amount, 'date': payment_date}],
            'late_fee': None
        }

        self.tenants.append(tenant)
        self.update_tenant_list_widget()

    def confirm_action(self, action, dialog):
        """Confirm an action and then perform it."""
        reply = QMessageBox.question(self, 'Confirm Action', 'Are you sure you want to perform this action?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            action()
            dialog.accept()  # Close the dialog after action is performed

    def update_tenant_list_widget(self):
        """Update the tenant list widget with the current tenants."""
        self.tenant_list_widget.clear()
        for tenant in self.tenants:
            tenant_info = f"{tenant['first_name']} {tenant['last_name']} - Apt: {tenant['apartment_number']}"
            self.tenant_list_widget.addItem(tenant_info)

    def open_update_tenant_form(self):
        """Open a form to update tenant info."""
        selected_item = self.tenant_list_widget.currentItem()
        if not selected_item:
            return

        tenant_info = selected_item.text()

        tenant_info_parts = tenant_info.split(" - ")
        if len(tenant_info_parts) < 2:
            return

        tenant_name = tenant_info_parts[0]
        apartment_number = tenant_info_parts[1].split(":")[1].strip()

        # Find the tenant to update
        tenant = None
        for t in self.tenants:
            if t['first_name'] + " " + t['last_name'] == tenant_name and t['apartment_number'] == apartment_number:
                tenant = t
                break

        if tenant:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Update Tenant: {tenant_name}")

            form_layout = QFormLayout()

            self.first_name_input = QLineEdit(tenant['first_name'], dialog)
            form_layout.addRow("First Name:", self.first_name_input)

            self.last_name_input = QLineEdit(tenant['last_name'], dialog)
            form_layout.addRow("Last Name:", self.last_name_input)

            self.apartment_input = QLineEdit(tenant['apartment_number'], dialog)
            form_layout.addRow("Apartment Number:", self.apartment_input)

            self.email_input = QLineEdit(tenant['email'], dialog)
            form_layout.addRow("Email:", self.email_input)

            self.phone_input = QLineEdit(tenant['phone'], dialog)
            form_layout.addRow("Phone Number:", self.phone_input)

            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(lambda: self.confirm_action(lambda: self.update_tenant(tenant), dialog))
            buttons.rejected.connect(dialog.reject)

            form_layout.addWidget(buttons)
            dialog.setLayout(form_layout)

            dialog.exec_()

    def update_tenant(self, tenant):
        """Update the tenant information."""
        tenant['first_name'] = self.first_name_input.text()
        tenant['last_name'] = self.last_name_input.text()
        tenant['apartment_number'] = self.apartment_input.text()
        tenant['email'] = self.email_input.text()
        tenant['phone'] = self.phone_input.text()

        self.update_tenant_list_widget()

    def delete_tenant(self):
        """Delete the selected tenant."""
        selected_item = self.tenant_list_widget.currentItem()
        if not selected_item:
            return

        tenant_info = selected_item.text()
        tenant_info_parts = tenant_info.split(" - ")
        tenant_name = tenant_info_parts[0]
        apartment_number = tenant_info_parts[1].split(":")[1].strip()

        # Find and remove the tenant
        tenant_to_delete = None
        for tenant in self.tenants:
            if tenant['first_name'] + " " + tenant['last_name'] == tenant_name and tenant['apartment_number'] == apartment_number:
                tenant_to_delete = tenant
                break

        if tenant_to_delete:
            self.tenants.remove(tenant_to_delete)

        self.update_tenant_list_widget()

    def open_add_note_form(self):
        """Open a form to add a note, complaint, late fee, or payment to the selected tenant."""
        selected_item = self.tenant_list_widget.currentItem()
        if not selected_item:
            return

        tenant_info = selected_item.text()
        tenant_name = tenant_info.split(" - ")[0]

        # Find the tenant to add a note
        tenant = None
        for t in self.tenants:
            if t['first_name'] + " " + t['last_name'] == tenant_name:
                tenant = t
                break

        if tenant:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Add Note for {tenant_name}")

            form_layout = QFormLayout()

            # Note input
            self.note_input = QTextEdit(dialog)
            form_layout.addRow("Note:", self.note_input)

            # Complaint input
            self.complaint_input = QLineEdit(dialog)
            form_layout.addRow("Complaint:", self.complaint_input)

            # Late fee input
            self.late_fee_input = QLineEdit(dialog)
            form_layout.addRow("Late Fee:", self.late_fee_input)

            # Payment input
            self.payment_amount_input = QLineEdit(dialog)
            form_layout.addRow("Payment Amount:", self.payment_amount_input)

            self.payment_date_input = QDateEdit(dialog)
            self.payment_date_input.setDate(QDate.currentDate())
            form_layout.addRow("Payment Date:", self.payment_date_input)

            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(lambda: self.add_note_to_tenant(tenant, dialog))
            buttons.rejected.connect(dialog.reject)

            form_layout.addWidget(buttons)
            dialog.setLayout(form_layout)

            dialog.exec_()

    def add_note_to_tenant(self, tenant, dialog):
        """Add the note to the tenant."""
        note = self.note_input.toPlainText()
        complaint = self.complaint_input.text()
        late_fee = self.late_fee_input.text()
        payment_amount = self.payment_amount_input.text()
        payment_date = self.payment_date_input.date().toString(Qt.ISODate)

        # Add the new information to the tenant
        if note:
            tenant['notes'].append(note)
        if complaint:
            tenant['complaints'].append(complaint)
        if late_fee:
            tenant['late_fee'] = late_fee  # Assuming a single late fee for simplicity
        if payment_amount:
            tenant['payments'].append({'amount': payment_amount, 'date': payment_date})

        # After adding, update the list of tenants and close the dialog
        self.update_tenant_list_widget()
        dialog.accept()

    def view_notes(self):
        """View the notes, complaints, payments, and late fee of the selected tenant."""
        selected_item = self.tenant_list_widget.currentItem()
        if not selected_item:
            return

        tenant_info = selected_item.text()
        tenant_name = tenant_info.split(" - ")[0]

        # Find the tenant to view notes
        tenant = None
        for t in self.tenants:
            if t['first_name'] + " " + t['last_name'] == tenant_name:
                tenant = t
                break

        if tenant:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Notes, Complaints, Payments for {tenant_name}")

            form_layout = QVBoxLayout()

            # Notes section
            notes_text = QTextEdit(dialog)
            notes_text.setReadOnly(True)
            notes_text.setPlainText("\n".join(tenant['notes']) if tenant['notes'] else "No notes available.")
            form_layout.addWidget(QLabel("Notes:"))
            form_layout.addWidget(notes_text)

            # Complaints section
            complaints_text = QTextEdit(dialog)
            complaints_text.setReadOnly(True)
            complaints_text.setPlainText("\n".join(tenant['complaints']) if tenant['complaints'] else "No complaints available.")
            form_layout.addWidget(QLabel("Complaints:"))
            form_layout.addWidget(complaints_text)

            # Payments section
            payments_text = QTextEdit(dialog)
            payments_text.setReadOnly(True)
            if tenant['payments']:
                payments_content = "\n".join([f"{p['amount']} on {p['date']}" for p in tenant['payments']])
            else:
                payments_content = "No payments recorded."
            payments_text.setPlainText(payments_content)
            form_layout.addWidget(QLabel("Payments:"))
            form_layout.addWidget(payments_text)

            # Late Fee section
            late_fee_text = QTextEdit(dialog)
            late_fee_text.setReadOnly(True)
            late_fee_text.setPlainText(tenant.get('late_fee', "No late fee recorded"))
            form_layout.addWidget(QLabel("Late Fee:"))
            form_layout.addWidget(late_fee_text)

            close_button = QPushButton("Close")
            close_button.clicked.connect(dialog.accept)
            form_layout.addWidget(close_button)

            dialog.setLayout(form_layout)
            dialog.exec_()

    def generate_report(self):
        """Generate a report of all tenants."""
        report = "\n\n".join([f"Name: {tenant['first_name']} {tenant['last_name']}\n"
                             f"Apt: {tenant['apartment_number']}\n"
                             f"Email: {tenant['email']}\n"
                             f"Phone: {tenant['phone']}\n"
                             f"Payments: {tenant['payments']}\n"
                             f"Notes: {tenant['notes']}\n"
                             f"Complaints: {tenant['complaints']}" for tenant in self.tenants])

        dialog = QDialog(self)
        dialog.setWindowTitle("Tenant Report")
        text_edit = QTextEdit(dialog)
        text_edit.setReadOnly(True)
        text_edit.setPlainText(report)
        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        dialog.setLayout(layout)
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ApartmentManagementApp()
    window.show()
    sys.exit(app.exec_())
