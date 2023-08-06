import json
from typing import Generator

from bs4 import BeautifulSoup


class OlxBaseParser:
    def __init__(self, soup: BeautifulSoup):
        """
        Parser base para todos os parsers derivados

        :param soup: Objeto SOAP para ser utilizado na busca de dados
        """
        self.soup = soup
        self.initial_data = self.__get_initial_data()
        self.ad_data = self._get_ad_data()

    def __iter__(self) -> Generator:
        """
        Implementa iterador para que seja possível aplica dict(Parser)

        :return: Tupla com nome do campo e valor
        """
        for item in dir(self):
            attr = getattr(self, item)
            if (
                not item.startswith("_")
                and item
                not in (
                    "initial_data",
                    "ad_data",
                    "soup",
                )
                and not callable(attr)
            ):
                yield item, getattr(self, item)

    def __getitem__(self, item):
        """
        Implementa getitem para que seja possível
        buscar atributo com Parser['atributo']

        :param item: Chave a ser buscada
        :return: Valor atrelado a chave
        """
        try:
            return getattr(self, item)
        except AttributeError:
            return None

    def _get_ad_data(self) -> dict:
        return self.initial_data.get("ad", {})

    def __get_initial_data(self) -> dict:
        tag = "script"
        options = {"id": "initial-data"}
        key = "data-json"
        return json.loads(self.soup.find(tag, options)[key])
