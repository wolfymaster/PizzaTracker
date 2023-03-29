import requests
import json
import random
import time

PORT = 8000


# Function to generate a random JSON payload
def generate_random_payload():
    total = round(random.uniform(1.00, 50.00), 2)
    num_items = random.randint(1, 5)
    items = []
    for i in range(num_items):
        name = f"item{i + 1}"
        price = round(random.uniform(0.01, 10.00), 2)
        quantity = random.randint(1, 10)
        item_total = round(price * quantity, 2)
        item = {"name": name, "price": price, "quantity": quantity, "total": item_total}
        items.append(item)
    payload = {"total": total, "items": items}
    return json.dumps(payload)


# Function to hit a random URL with a random payload at random intervals
def hit_url():
    url = f"http://localhost:{PORT}/create"
    payload = generate_random_payload()
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=payload, headers=headers)
        print(f"URL: {url}\nPayload: {payload}\nResponse: {response.text}")
    except requests.exceptions.RequestException as e:
        print(e)


while True:
    hit_url()
    time.sleep(random.randint(5, 15))
