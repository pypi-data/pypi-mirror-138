import requests


class Client:
    USERNAME = None
    PASSWORD = None
    URL = None

    def __init__(self, username: str, password: str, url: str) -> None:
        self.USERNAME = username
        self.PASSWORD = password
        self.URL = url

    def aggregated_base_query(self, plate: str):
        path = "/Consultas/consultaBaseAgregados.json"
        params = f"usuario={self.USERNAME}&senha={self.PASSWORD}&placa={plate}"

        return requests.get(f"{self.URL}{path}?{params}")
