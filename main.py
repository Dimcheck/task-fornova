import httpx
import json
import sys
from decimal import Decimal


FILE_ID = "1x_7pO8aFl9VIWOFVj4P33DyZGENq0y1i"       # in real world scenarion should have been placed in .env
URL = "https://drive.google.com/uc?export=download" # in real world scenarion should have been placed in .env


def download_the_file(FILE_ID: str = FILE_ID, destination: str = "Python-task.json"):
    """
    downloads JSON file to the same directory as py file
    """
    transport = httpx.HTTPTransport(retries=3)
    client = httpx.Client(transport=transport, follow_redirects=True)

    with client.stream("GET", URL, params={"id": FILE_ID}) as response:
        CHUNK_SIZE = 10000
        with open(destination, "wb") as f:
            for chunk in response.iter_bytes(CHUNK_SIZE):
                if chunk:
                    f.write(chunk)


def read_the_file(filepath: str = "Python-task.json") -> dict:
    """
    returns serialized data from the JSON file
    that supposed to be in the same directory as py file
    """
    try:
        with open(filepath, "r") as file_data:
            data = json.load(file_data)
            return data
    except Exception as error:
        print(f"Correct file was not provided: {error}")
        sys.exit(1)


def extract_cheapest_room_and_price(data: dict = None) -> tuple:
    """
    func returns the cheapest (lowest) shown_price
    """
    assignment_results = data.get("assignment_results")[0]
    cheapest_price, cheapest_room = 0, 0

    for x, y in assignment_results.get("shown_price").items():
        if Decimal(y) < cheapest_price:
            cheapest_price = Decimal(y)
            cheapest_room = x
        else:
            cheapest_price = Decimal(y)
            cheapest_room = x

    return (cheapest_room, float(cheapest_price))


def extract_cheapest_room_number_of_guests_price(data: dict = None) -> tuple:
    """
    func returns the room type, number of guest with the cheapest price
    """
    assignment_results = data.get("assignment_results")[0]
    number_of_guest = assignment_results.get("number_of_guests")
    cheapest_room, cheapest_price = extract_cheapest_room_and_price(data)

    return (cheapest_room, number_of_guest, cheapest_price)


def extract_total_price(data: dict = None) -> dict:
    """
    func returns total price for all rooms along with the room type
    by calculating SUM of NET PRICE & TAXES
    """
    total_price = {}
    assignment_results = data.get("assignment_results")[0]
    ext_data = assignment_results.get("ext_data")
    tax = sum([Decimal(x) for x in json.loads(ext_data.get("taxes")).values()])

    for x, y in assignment_results.get("net_price").items():
        total_price[x] = float(Decimal(y) + tax)

    return total_price


def make_output():
    """
    func returns all data for test task completion and save into file
    """
    json_data = read_the_file()
    task_a = extract_cheapest_room_and_price(json_data)[1]
    task_b = extract_cheapest_room_number_of_guests_price(json_data)
    task_c = extract_total_price(json_data)

    with open("output.json", "w") as file:
        json.dump(
            (
                {"the cheapest (lowest) shown price": task_a},
                {"the room type, number of guest with the cheapest price": task_b},
                {"the total price(including tax) for all rooms along with the room type": task_c},
            ), file
        )


if __name__ == "__main__":
    download_the_file()
    make_output()

