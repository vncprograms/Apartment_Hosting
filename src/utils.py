import re
from datetime import datetime

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def calculate_late_fee(payment_date, current_date):
    payment_date = datetime.strptime(payment_date, '%Y-%m-%d')
    if (current_date - payment_date).days > 30:
        return (current_date - payment_date).days * 2
    return 0
