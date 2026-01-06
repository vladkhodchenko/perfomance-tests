from clients.http.client import HTTPClient
from httpx import Response
from locust.env import Environment
from clients.http.gateway.client import (
    build_gateway_http_client,
    build_gateway_locust_http_client
)
from clients.http.gateway.cards.schema import (
    IssueVirtualCardRequestSchema,
    IssuePhysicalCardRequestSchema,
    IssuePhysicalCardResponseSchema,
    IssueVirtualCardResponseSchema
)
from tools.routes import APIRoutes


class CardsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/cards сервиса http-gateway.
    """
    def issue_virtual_card_api(self, request: IssueVirtualCardRequestSchema) -> Response:
        """
        Создание виртуальной карты.

        :param request: Словарь с данными виртуальной карты.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post(f"{APIRoutes.CARDS}/issue-virtual-card", json=request.model_dump(by_alias=True))

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestSchema) -> Response:
        """
        Создание физической карты.

        :param request: Словарь с данными физической карты.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post(f"{APIRoutes.CARDS}/issue-virtual-card", json=request.model_dump(by_alias=True))

    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseSchema:
        request = IssueVirtualCardRequestSchema(
            user_id=user_id,
            account_id=account_id
        )
        response = self.issue_virtual_card_api(request)
        return IssueVirtualCardResponseSchema.model_validate_json(response.text)

    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseSchema:
        request = IssuePhysicalCardRequestSchema(
            user_id=user_id,
            account_id=account_id
        )
        response = self.issue_physical_card_api(request)
        return IssuePhysicalCardResponseSchema.model_validate_json(response.text)


def build_cards_gateway_http_client(environment: Environment) -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(client=build_gateway_http_client(environment))


def build_cards_gateway_locust_http_client(environment: Environment) -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр CardsGatewayHTTPClient с хуками сбора метрик.
    """
    return CardsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))