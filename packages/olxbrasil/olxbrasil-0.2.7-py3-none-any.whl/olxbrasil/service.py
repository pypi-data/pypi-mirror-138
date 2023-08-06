from typing import Any, Dict, Optional

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from httpx import AsyncClient, Client, ConnectError, HTTPStatusError

from olxbrasil.constants import CATEGORIES
from olxbrasil.exceptions import OlxRequestError
from olxbrasil.filters import Filter, LocationFilter
from olxbrasil.parsers import ItemParser, ListParser

user_agent = UserAgent()


class Olx:
    def __init__(
        self,
        *,
        category: str,
        subcategory: Optional[str] = None,
        location: Optional[LocationFilter] = None,
        filters: Optional[Filter] = None,
    ):
        """
        Parser síncrono para OLX Brasil
        :param category: Categoria utilizada na busca da OLX
        :param subcategory: Subcategoria utilizada na
        busca da OLX, deve pertencer a categoria
        :param location: Objeto de filtro de localidade
        :param filters: Objeto de filtro de parametros
        """
        if not location:
            self.location = None
            self.subdomain = "www"
        else:
            self.location = location
            self.subdomain = self.location.state.lower()
        self.user_agent = user_agent
        self.category = None
        self.subcategory = None
        self.client = Client(
            base_url=f"https://{self.subdomain}.olx.com.br",
            headers={"User-Agent": self.user_agent.random},
        )
        self.filters = filters

        valid_category = category in CATEGORIES.keys()

        if valid_category:
            valid_subcategory = (
                subcategory in CATEGORIES[category]["subcategories"].keys()
            )
            self.category = CATEGORIES[category]["category"]

            if subcategory and valid_subcategory:
                sub = CATEGORIES[category]["subcategories"][subcategory]
                self.subcategory = sub

            if subcategory and not valid_subcategory:
                raise ValueError(
                    f"{subcategory} is not a valid subcategory, "
                    "please provide a valid subcategory: "
                    f"{' '.join(CATEGORIES[category]['subcategories'].keys())}"
                )
        else:
            raise ValueError(
                f"{category} is not a valid category, "
                "please provide a valid category: "
                f"{' '.join(CATEGORIES.keys())}"
            )

    def build_url(self) -> str:
        url = ""
        if self.location:
            url += self.location.get_endpoint()

        url += f"/{self.category}"

        if self.subcategory:
            url += f"/{self.subcategory}"

        if self.filters:
            url += self.filters.get_endpoint()

        return url

    def fetch_all(self, page=0) -> Dict[str, Any]:
        parameters = {"o": min(page, 100)}
        url = self.build_url()

        if self.filters:
            parameters = self.filters.get_filters(parameters)

        try:
            response = self.client.get(url, params=parameters)

            response.raise_for_status()
        except HTTPStatusError as err:
            raise OlxRequestError(
                "Was not possible to reach OLX server"
            ) from err

        soup = BeautifulSoup(response.text, "html.parser")

        parser = ListParser(soup)

        return parser.items

    def fetch_item(self, url: str) -> ItemParser:
        try:
            response = self.client.get(url)

            response.raise_for_status()
        except (HTTPStatusError, ConnectError) as err:
            raise OlxRequestError(
                "Was not possible to reach OLX server"
            ) from err

        soup = BeautifulSoup(response.text, "html.parser")
        parser = ItemParser(soup)
        return parser


class AsyncOlx(Olx):
    def __init__(
        self,
        *,
        category: str,
        subcategory: Optional[str] = None,
        location: Optional[LocationFilter] = None,
        filters: Optional[Filter] = None,
    ):
        super().__init__(
            category=category,
            subcategory=subcategory,
            location=location,
            filters=filters,
        )
        self.__base_url: str = f"https://{self.subdomain}.olx.com.br"
        self.__headers: Dict[str, str] = {"User-Agent": self.user_agent.random}

    async def fetch_all(  # type: ignore
        self, page: Optional[int] = 0
    ) -> Dict[str, Any]:
        parameters = {"o": min(page, 100)}  # type: ignore
        url = self.build_url()

        if self.filters:
            parameters = self.filters.get_filters(parameters)

        try:
            async with AsyncClient(
                base_url=self.__base_url,
                headers=self.__headers,
            ) as client:
                response = await client.get(url, params=parameters)

            response.raise_for_status()
        except (HTTPStatusError, ConnectError) as err:
            raise OlxRequestError(
                "Was not possible to reach OLX server"
            ) from err

        soup = BeautifulSoup(response.text, "html.parser")

        parser = ListParser(soup)

        return parser.items

    async def fetch_item(self, url: str) -> ItemParser:  # type: ignore
        try:
            async with AsyncClient(
                base_url=self.__base_url,
                headers=self.__headers,
            ) as client:
                response = await client.get(url)

                response.raise_for_status()
        except (HTTPStatusError, ConnectError) as err:
            raise OlxRequestError(
                "Was not possible to reach OLX server"
            ) from err

        soup = BeautifulSoup(response.text, "html.parser")
        parser = ItemParser(soup)
        return parser
