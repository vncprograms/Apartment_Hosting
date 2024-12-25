function rentApartment(apartmentId) {
    fetch(`/rent_apartment/${apartmentId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ apartment_id: apartmentId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Apartment rented successfully');
        } else {
            alert('Failed to rent the apartment');
        }
    })
    .catch(error => console.error('Error:', error));
}
