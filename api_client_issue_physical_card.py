from clients.http.gateway.users.client import build_users_gateway_http_client
from clients.http.gateway.cards.client import build_cards_gateway_http_client
from clients.http.gateway.accounts.client import build_accounts_gateway_http_client


users_gateway_client = build_users_gateway_http_client()
cards_gateway_client = build_cards_gateway_http_client()
accounts_gateway_client = build_accounts_gateway_http_client()

create_user_response = users_gateway_client.create_user()
print("create_user_response", create_user_response)

open_debit_card_account_response = accounts_gateway_client.open_debit_card_account(
    user_id = create_user_response["user"]["id"]
)
print("open_debit_card_account_response", open_debit_card_account_response)


issue_virtual_card_response = cards_gateway_client.issue_virtual_card(
    user_id=create_user_response["user"]["id"],
    account_id=open_debit_card_account_response["account"]["id"]
)
print("issue_virtual_card_response", issue_virtual_card_response)