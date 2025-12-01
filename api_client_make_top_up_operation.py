from clients.http.gateway.users.client import build_users_gateway_http_client
from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.operations.client import build_operations_gateway_http_client


users_gateway_client = build_users_gateway_http_client()
accounts_gateway_client = build_accounts_gateway_http_client()
operations_gateway_client = build_operations_gateway_http_client()

create_user_response = users_gateway_client.create_user()
open_debit_card_account_response = accounts_gateway_client.open_debit_card_account(
    user_id = create_user_response["user"]["id"]
)
make_top_up_operation_response = operations_gateway_client.make_top_up_operation(
    account_id=open_debit_card_account_response["account"]["id"],
    card_id=open_debit_card_account_response["account"]["cards"][0]["id"]
)

print("Create user response:", create_user_response)
print("Open debit card account response:", open_debit_card_account_response)
print("Make top up operation response:", make_top_up_operation_response)