import grpc

from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub
from contracts.services.gateway.accounts.rpc_open_savings_account_pb2 import OpenSavingsAccountRequest, OpenSavingsAccountResponse
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from contracts.services.gateway.documents.rpc_get_contract_document_pb2 import GetContractDocumentRequest, GetContractDocumentResponse
from contracts.services.gateway.documents.rpc_get_tariff_document_pb2 import GetTariffDocumentResponse,GetTariffDocumentRequest
from contracts.services.gateway.documents.documents_gateway_service_pb2_grpc import DocumentsGatewayServiceStub
from tools.fakers import fake


channel = grpc.insecure_channel("localhost:9003")

users_gateway_service = UsersGatewayServiceStub(channel)
accounts_gateway_service = AccountsGatewayServiceStub(channel)
documents_gateway_client = DocumentsGatewayServiceStub(channel)

create_user_request = CreateUserRequest(
    email=fake.email(),
    last_name=fake.last_name(),
    first_name=fake.first_name(),
    middle_name=fake.middle_name(),
    phone_number=fake.phone_number()
)
create_user_response: CreateUserResponse = users_gateway_service.CreateUser(create_user_request)

open_savings_account_request = OpenSavingsAccountRequest(user_id=create_user_response.user.id)
open_savings_account_response: OpenSavingsAccountResponse = accounts_gateway_service.OpenSavingsAccount(open_savings_account_request)

get_tariff_document_request = GetTariffDocumentRequest(account_id=open_savings_account_response.account.id)
get_tariff_document_response: GetTariffDocumentResponse = documents_gateway_client.GetTariffDocument(get_tariff_document_request)

get_contract_document_request = GetContractDocumentRequest(account_id=open_savings_account_response.account.id)
get_contract_document_response: GetContractDocumentResponse = documents_gateway_client.GetContractDocument(get_contract_document_request)


print("Create user response:", create_user_response)
print("Open savings account response:", open_savings_account_response)
print("Get tariff document response:", get_tariff_document_response)
print("Get contract document response:", get_contract_document_response)
