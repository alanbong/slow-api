# views.py
from core.templator import render

def get_data_from_file(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(line.strip().split('::'))
    return data

def home_view():
    body = 'home'
    return '200 OK', [('Content-Type', 'text/html')], body

def users_list_view():
    users_data = get_data_from_file('data/users.txt')
    users = [{'id': user[0], 'name': user[1]} for user in users_data]
    context = {'users': users}

    template = """
    <h1>Our users:</h1>
    <ul>
        {% for user in users %}
            <li>ID: {{ user.id }}, Name: {{ user.name }}</li>
        {% endfor %}
    </ul>
    """
    body = render(template, context).encode('utf-8')
    return '200 OK', [('Content-Type', 'text/html')], body

def user_detail_view(user_id):
    all_cars = get_data_from_file('data/cars.txt')
    user_cars = [
        {'id': car[0], 'brand': car[2], 'model': car[3], 'plate': car[4]} 
        for car in all_cars if int(car[1]) == user_id
    ]
    context = {'cars': user_cars}
    template = """
    <h1>Your cars:</h1>
    <ul>
        {% for car in cars %}
            <li>{{ car.brand }} {{ car.model }} ({{ car.plate }})</li>
        {% endfor %}
    </ul>
    """

    body = render(template, context).encode('utf-8')
    return '200 OK', [('Content-Type', 'text/html')], body

def not_found_view():
    return (
        '404 Not Found',
        [('content-type', 'text/html')],
        'Not Found'
    )

def method_not_allowed(allowed_methods=None):
    return (
        '405 Method Not Allowed',
        [('content-type', 'text/html')],
        f'Allowed methods: {allowed_methods}'
    )
