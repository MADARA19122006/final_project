from requests import get

print(get('http://localhost:5000/api/booking_get',
           json={'check_in_from': '20210301', 'check_in_to': '20210506'}).json())
