import os
from typing import Optional

import grpc

from bridgecard_core_sdk.core.core_db.schema.base_schema import EnvironmentEnum

from .protos import billing_details_pb2_grpc, billing_details_pb2

from .model import BillType

from .utils.billing_service_data_context import billing_service_data_context


def init_billing_service():
    client_private_key = os.environ.get("BRIDGECARD_ISSUING_TLS_CLIENT_PRIVATE_KEY")

    client_certificate_chain = os.environ.get(
        "BRIDGECARD_ISSUING_TLS_CLIENT_CERT_CHAIN"
    )

    server_certificate_chain = os.environ.get(
        "BRIDGECARD_ISSUING_TLS_SERVER_CERT_CHAIN"
    )

    server_addr = (
        "ae740cdf8e16b48bc82a259400ca03b9-1383199310.us-west-2.elb.amazonaws.com:80"
    )

    # server_addr = "0.0.0.0:8089"

    # creds = grpc.ssl_channel_credentials(
    #     private_key=client_private_key.encode(),
    #     certificate_chain=client_certificate_chain.encode(),
    #     root_certificates=server_certificate_chain.encode(),
    # )
    # grpc_channel = grpc.secure_channel(server_addr, creds)

    grpc_channel = grpc.insecure_channel(server_addr)

    billing_service_data_context.grpc_channel = grpc_channel


def check_admin_bill_status(
    token: str,
    bill_type: BillType,
    card_id: Optional[str] = None,
    transaction_amount: Optional[str] = None,
    account_id: Optional[str] = None,
    cardholder_id: Optional[str] = None,
    environment: Optional[EnvironmentEnum] = None,
):
    grpc_channel = billing_service_data_context.grpc_channel

    client_stub = billing_details_pb2_grpc.BillingServiceStub(grpc_channel)

    metadata = (("token", token),)

    request = billing_details_pb2.RequestData(
        bill_type=bill_type,
        request_metadata={
            "account_id": account_id or "",
            "cardholder_id": cardholder_id or "",
            "card_id": card_id or "",
            "transaction_amount": transaction_amount or "",
            "environment": environment or "",
        },
    )

    try:
        response = client_stub.CheckAdminBillStatus(request, metadata=metadata)

        if response.code == grpc.StatusCode.OK.value[0]:
            amount_out = response.response_metadata.get("amount_out") or 0

            return amount_out

    except grpc.RpcError as e:
        print(f"check_admin_bill_status - Code: {e.code()}")

        print(f"check_admin_bill_status - Message: {e.details()}")

        return False


def bill_admin(
    token: str,
    bill_type: BillType,
    card_id: Optional[str] = None,
    transaction_amount: Optional[str] = None,
    account_id: Optional[str] = None,
    cardholder_id: Optional[str] = None,
    environment: Optional[EnvironmentEnum] = None,
):
    grpc_channel = billing_service_data_context.grpc_channel

    client_stub = billing_details_pb2_grpc.BillingServiceStub(grpc_channel)

    metadata = (("token", token),)

    # Make a remote gRPC call
    request = billing_details_pb2.RequestData(
        bill_type=bill_type,
        request_metadata={
            "account_id": account_id or "",
            "cardholder_id": cardholder_id or "",
            "card_id": card_id or "",
            "transaction_amount": transaction_amount or "",
            "environment": environment or "",
        },
    )

    try:
        response = client_stub.BillAdmin(request, metadata=metadata)

        if response.code == grpc.StatusCode.OK.value[0]:
            return True

    except grpc.RpcError as e:
        print(f"bill_admin - Code: {e.code()}")

        print(f"bill_admin - Message: {e.details()}")

        return False
