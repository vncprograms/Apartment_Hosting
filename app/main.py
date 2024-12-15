import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import init_db
from app.tenant import add_tenant, get_tenant_payments
from app.apartment import add_apartment
from app.payment import add_payment
from app.note import add_note

def main():
    # Initialize the database (creates tables if they don't exist)
    init_db()

    # Add an apartment (you can add more or modify details)
    apartment_id = add_apartment(rent_price=1200.00, utilities_price=150.00)

    # Add tenants for that apartment
    tenant_id_1 = add_tenant(name="John AppleSeed", 
                             lease_start_date="2024-01-01", 
                             lease_end_date="2025-01-01", 
                             deposit=1200.00, 
                             apartment_id=apartment_id)
    tenant_id_2 = add_tenant(name="Jane Doe", 
                             lease_start_date="2024-02-01", 
                             lease_end_date="2025-02-01", 
                             deposit=1000.00, 
                             apartment_id=apartment_id)

    # Add payments for tenants (you can modify these as well)
    add_payment(tenant_id_1, amount=1200.00, month="January", year=2024, payment_date="2024-01-01")
    add_payment(tenant_id_1, amount=1200.00, month="February", year=2024, payment_date="2024-02-01")
    
    add_payment(tenant_id_2, amount=1000.00, month="February", year=2024, payment_date="2024-02-01")

    # Add some notes (e.g., complaints or maintenance requests)
    add_note(tenant_id_1, note_type="Complaint", note_description="Noise disturbance at night", date_added="2024-01-15")
    add_note(tenant_id_2, note_type="Maintenance", note_description="Leaky faucet", date_added="2024-02-10")

    # Retrieve and print the payment history for each tenant
    print(f"Payments for John AppleSeed:")
    payments_1 = get_tenant_payments(tenant_id_1)
    for payment in payments_1:
        print(payment)

    print(f"\nPayments for Jane Doe:")
    payments_2 = get_tenant_payments(tenant_id_2)
    for payment in payments_2:
        print(payment)

    # Optionally, you can also query and display other tenant information or notes
    # This example is printing out all notes for John AppleSeed
    print(f"\nNotes for John AppleSeed:")
    # Retrieve notes (assuming you have a function for retrieving them)
    # For simplicity, you would add similar functions like get_tenant_notes if necessary

if __name__ == "__main__":
    main()
