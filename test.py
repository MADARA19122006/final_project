from requests import post

print(post('http://localhost:5000/api/availability',
           json={'date': '20210503', 'room': 1, 'quantity_rooms': 4,
                 'price': 3000}).json())
