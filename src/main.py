from PyQt5.QtWidgets import QApplication
import sys
from ui import ApartmentManagementApp
from database import create_tables

def main():
    # Create the database tables if they don't exist
    create_tables()

    app = QApplication(sys.argv)
    window = ApartmentManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
