import abc
from typing import Dict, Iterable, Optional, Union

from olxbrasil.constants import LOCATIONS_URL
from olxbrasil.exceptions import FilterNotFoundError
from olxbrasil.utils import build_boolean_parameters, build_search_parameters


class Filter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_filters(self, params: Optional[Dict] = None) -> Dict:
        pass  # pragma: nocover

    @abc.abstractmethod
    def get_endpoint(self) -> str:
        pass  # pragma: nocover


class ItemFilter(Filter):
    def __init__(
        self,
        *,
        manufacturer: Optional[str] = None,
        model: Optional[str] = None,
        boolean_filters: Optional[Iterable] = tuple(),
        search_filters: Optional[Dict] = None,
    ):
        """
        Filtro de items

        :param manufacturer: Fabricante do carro (Aplicável somente a veículos)
        :param model: Modelo do carro (Aplicável somente a veículos)
        :param boolean_filters: Filtros de ativo/inativo
        :param search_filters: Filtros de busca,
        como valor minimo ou valor maximo
        """
        self.__manufacturer = manufacturer
        self.__model = model
        self.__boolean_filters = boolean_filters
        self.__search_filters = search_filters

    def get_filters(self, params: Optional[Dict] = None) -> Dict:
        """
        Formata os filtros para o formato esperado pela OLX

        :param params: Parametros para serem formatados
        :return: Dicionário com os parametros
        para ser utilizado na formação da URL
        """
        item_filter = params or {}
        if self.__boolean_filters:
            item_filter.update(
                build_boolean_parameters(*self.__boolean_filters)
            )
        if self.__search_filters:
            item_filter.update(
                build_search_parameters(**self.__search_filters)
            )

        return item_filter

    def get_endpoint(self) -> str:
        """
        Em caso de veículo retorna o endpoint
        para ser utilizado na formação da URL

        :return: Endpoint para ser utilizado na formação da URL
        """
        endpoint = ""

        if self.__manufacturer:
            endpoint += f"/{self.__manufacturer.lower()}"
            if self.__model:
                endpoint += f"/{self.__model.lower()}"

        return endpoint


class LocationFilter(Filter):
    def __init__(self, state: str, ddd: Optional[Union[int, float]] = None):
        """
        Filtro de localização

        :param state: Estado onde vai ser feito a busca
        :param ddd: DDD da região da busca,
        tem que ser um DDD pertencente ao estado escolhido
        """
        self.state = state.upper()
        self.__ddd = ddd
        self.__validate()

    def __validate(self) -> bool:
        """Valida se o estado existe e se o DDD pertence ao estado escolhido"""
        if self.state not in LOCATIONS_URL:
            raise FilterNotFoundError(f"State {self.state} not found")
        if self.__ddd and self.__ddd not in LOCATIONS_URL[self.state]:
            raise FilterNotFoundError(
                f"DDD {self.__ddd} was not found in state {self.state}"
            )

        return True

    def get_filters(
        self, params: Optional[Dict] = None
    ) -> Dict:  # pragma: nocover
        pass

    def get_endpoint(self) -> str:
        """Retorna o endpoint da localização
        para ser utilizado na formatação da URL"""
        if self.__ddd:
            return LOCATIONS_URL[self.state][self.__ddd]
        return ""
