from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget, QDialog, QFormLayout, QDialogButtonBox, QTextEdit, QDateEdit, QMessageBox, QTabWidget, QGridLayout, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QDate
import sys
import json  # For saving data

class ApartmentManagementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Apartment Management System")
        self.setGeometry(100, 100, 900, 600)

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

        self.layout = QVBoxLayout(self)

        # Tab Widget to organize different sections
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Tenant Management Tab
        self.tenant_management_tab = QWidget()
        self.tabs.addTab(self.tenant_management_tab, "Tenant Management")

        tenant_layout = QVBoxLayout(self.tenant_management_tab)
        tenant_layout.addWidget(QLabel("Tenant List:"))
        
        self.tenant_list_widget = QListWidget(self)
        tenant_layout.addWidget(self.tenant_list_widget)
        
        # Buttons for tenant management
        button_layout = QHBoxLayout()
        
        self.add_tenant_button = QPushButton("Add Tenant", self)
        self.add_tenant_button.clicked.connect(self.open_add_tenant_form)
        button_layout.addWidget(self.add_tenant_button)
        
        self.update_tenant_button = QPushButton("Update Tenant", self)
        self.update_tenant_button.clicked.connect(self.open_update_tenant_form)
        button_layout.addWidget(self.update_tenant_button)
        
        self.delete_tenant_button = QPushButton("Delete Tenant", self)
        self.delete_tenant_button.clicked.connect(self.delete_tenant)
        button_layout.addWidget(self.delete_tenant_button)
        
        tenant_layout.addLayout(button_layout)

        # Notes & Payments Tab
        self.notes_payments_tab = QWidget()
        self.tabs.addTab(self.notes_payments_tab, "Notes & Payments")

        notes_layout = QVBoxLayout(self.notes_payments_tab)
        self.view_notes_button = QPushButton("View Notes/Complaints/Payments", self)
        self.view_notes_button.clicked.connect(self.view_notes)
        notes_layout.addWidget(self.view_notes_button)

        self.add_note_button = QPushButton("Add Note/Complaint/Payment", self)
        self.add_note_button.clicked.connect(self.open_add_note_form)
        notes_layout.addWidget(self.add_note_button)

        # Report Tab
        self.report_tab = QWidget()
        self.tabs.addTab(self.report_tab, "Reports")

        report_layout = QVBoxLayout(self.report_tab)
        self.report_button = QPushButton("Generate Report", self)
        self.report_button.clicked.connect(self.generate_report)
        report_layout.addWidget(self.report_button)

        # Load tenant data
        self.load_tenant_data()

    def open_add_tenant_form(self):
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
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        apartment_number = self.apartment_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        payment_amount = self.payment_input.text()
        payment_date = self.payment_date_input.date().toString(Qt.ISODate)

        # Validation
        if not first_name or not last_name or not apartment_number or not email or not phone:
            QMessageBox.warning(self, "Error", "All fields must be filled!")
            return

        # Prevent duplicates
        for tenant in self.tenants:
            if tenant['first_name'] == first_name and tenant['last_name'] == last_name and tenant['apartment_number'] == apartment_number:
                QMessageBox.warning(self, "Error", "Tenant already exists!")
                return

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
        self.save_tenant_data()

    def update_tenant_list_widget(self):
        self.tenant_list_widget.clear()
        for tenant in self.tenants:
            tenant_info = f"{tenant['first_name']} {tenant['last_name']} - Apt: {tenant['apartment_number']}"
            self.tenant_list_widget.addItem(tenant_info)

    def save_tenant_data(self):
        """Save tenant data to a file."""
        with open('tenants.json', 'w') as file:
            json.dump(self.tenants, file, indent=4)

    def load_tenant_data(self):
        """Load tenant data from a file."""
        try:
            with open('tenants.json', 'r') as file:
                self.tenants = json.load(file)
            self.update_tenant_list_widget()
        except FileNotFoundError:
            pass

    def confirm_action(self, action, dialog):
        reply = QMessageBox.question(self, 'Confirm Action', 'Are you sure you want to perform this action?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            action()
            dialog.accept()

    def delete_tenant(self):
        selected_item = self.tenant_list_widget.currentItem()
        if not selected_item:
            return

        tenant_info = selected_item.text()
        tenant_name = tenant_info.split(" - ")[0]
        apartment_number = tenant_info.split(" - ")[1].split(":")[1].strip()

        tenant_to_delete = None
        for tenant in self.tenants:
            if tenant['first_name'] + " " + tenant['last_name'] == tenant_name and tenant['apartment_number'] == apartment_number:
                tenant_to_delete = tenant
                break

        if tenant_to_delete:
            self.tenants.remove(tenant_to_delete)
            self.update_tenant_list_widget()
            self.save_tenant_data()

    def view_notes(self):
        selected_item = self.tenant_list_widget.currentItem()
        if not selected_item:
            return

        tenant_info = selected_item.text()
        tenant_name = tenant_info.split(" - ")[0]

        tenant = next((t for t in self.tenants if t['first_name'] + " " + t['last_name'] == tenant_name), None)
        if tenant:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Notes/Complaints/Payments for {tenant_name}")

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
