class RestAPI:
    def __init__(self, url: str, key: str):
        self.api_url = f'{url}{key}'
