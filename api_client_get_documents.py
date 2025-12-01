from clients.http.gateway.users.client import build_users_gateway_http_client
from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.documents.client import build_documents_gateway_http_client


users_gateway_client = build_users_gateway_http_client()
accounts_gateway_client = build_accounts_gateway_http_client()
documents_gateway_client = build_documents_gateway_http_client()

create_user_response = users_gateway_client.create_user()
open_debit_card_account_response = accounts_gateway_client.open_debit_card_account(
    user_id = create_user_response["user"]["id"]
)
get_tariff_document_response = documents_gateway_client.get_tariff_document(
    account_id=open_debit_card_account_response["account"]["id"]
)
get_contract_document_response = documents_gateway_client.get_contract_document(
    account_id=open_debit_card_account_response["account"]["id"]
)

print(create_user_response)
print(open_debit_card_account_response)
print(get_tariff_document_response)
print(get_contract_document_response)