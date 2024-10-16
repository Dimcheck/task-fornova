import json
import sys
from decimal import Decimal


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

    return (cheapest_room, cheapest_price)


def extract_cheapest_room_number_of_guests_price(data: dict = None) -> tuple:
    """
    func returns the room type, number of guest with the cheapest price
    """
    assignment_results = data.get("assignment_results")[0]
    number_of_guest = assignment_results.get("number_of_guests")
    cheapest_suite = extract_cheapest_room_and_price(data)
    cheapest_room, cheapest_price = cheapest_suite[0], cheapest_suite[1]

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
        total_price[x] = Decimal(y) + tax

    return total_price

