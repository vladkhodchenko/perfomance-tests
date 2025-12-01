import time
from clients.http.gateway.users.client import (
    CreateUserRequestDict,
    build_users_gateway_http_client
)


users_gateway_client = build_users_gateway_http_client()

create_user_response = users_gateway_client.create_user()
print(create_user_response)

get_user_response = users_gateway_client.get_user(create_user_response["user"]["id"])

print(get_user_response)