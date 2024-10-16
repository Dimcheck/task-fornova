import httpx

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

