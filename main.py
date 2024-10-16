from downloader import download_the_file
from extractor import (
    read_the_file,
    extract_cheapest_room_and_price,
    extract_cheapest_room_number_of_guests_price,
    extract_total_price,
)


if __name__ == "__main__":
    download_the_file()
    json_data = read_the_file()
    task_a = extract_cheapest_room_and_price(json_data)[1]
    task_b = extract_cheapest_room_number_of_guests_price(json_data)
    task_c = extract_total_price(json_data)

    print(
        f"the cheapest (lowest) shown price: {task_a}", "\n\n",
        f"the room type, number of guest with the cheapest price: {task_b}", "\n\n",
        f"the total price(including tax) for all rooms along with the room type: {task_c}",
    )
