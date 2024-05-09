import os
from typing import Dict, Optional

import grpc

from google.protobuf.struct_pb2 import Struct

from .protos import (
    transaction_monitoring_details_pb2_grpc,
    transaction_monitoring_details_pb2,
)

from .model import ProductType

from .utils.transaction_monitoring_service_data_context import (
    transaction_monitoring_service_data_context,
)


def init_transaction_monitoring_service():
    client_private_key = os.environ.get(
        "BRIDGECARD_ISSUING_TLS_CLIENT_PRIVATE_KEY")

    client_certificate_chain = os.environ.get(
        "BRIDGECARD_ISSUING_TLS_CLIENT_CERT_CHAIN"
    )

    server_certificate_chain = os.environ.get(
        "BRIDGECARD_ISSUING_TLS_SERVER_CERT_CHAIN"
    )

    server_addr = (
        "a08c5b25f952f4266b52c70600aefcec-2060662335.us-west-2.elb.amazonaws.com:80"
    )
    server_addr = "localhost:8085"

    # creds = grpc.ssl_channel_credentials(
    #     private_key=client_private_key.encode(),
    #     certificate_chain=client_certificate_chain.encode(),
    #     root_certificates=server_certificate_chain.encode(),
    # )
    # grpc_channel = grpc.secure_channel(server_addr, creds)

    grpc_channel = grpc.insecure_channel(server_addr)

    transaction_monitoring_service_data_context.grpc_channel = grpc_channel


def check_transaction_risk(
    token: str,
    product_type: ProductType,
    data: Optional[Dict] = None,
):
    grpc_channel = transaction_monitoring_service_data_context.grpc_channel

    client_stub = (
        transaction_monitoring_details_pb2_grpc.TransactionMonitoringServiceStub(
            grpc_channel
        )
    )

    metadata = (("token", token),)

    metadata_struct = Struct()
    metadata_struct.update(data or {})

    request = transaction_monitoring_details_pb2.RequestData(
        product_type=product_type,
        request_metadata=metadata_struct,
    )

    try:
        response = client_stub.CheckTransactionRisk(request, metadata=metadata)

        if response.code == grpc.StatusCode.OK.value[0]:
            return True

    except grpc.RpcError as e:
        print(f"check_transaction_risk - Code: {e.code()}")

        print(f"check_transaction_risk - Message: {e.details()}")

        return False


def whitelist_user_from_potential_fraud(
    token: str,
    product_type: ProductType,
    data: Optional[Dict] = None,
):
    grpc_channel = transaction_monitoring_service_data_context.grpc_channel

    client_stub = (
        transaction_monitoring_details_pb2_grpc.TransactionMonitoringServiceStub(
            grpc_channel
        )
    )

    metadata = (("token", token),)

    metadata_struct = Struct()
    metadata_struct.update(data or {})

    request = transaction_monitoring_details_pb2.RequestData(
        product_type=product_type,
        request_metadata=metadata_struct,
    )

    try:
        response = client_stub.WhitelistUserFromPotentialFraud(
            request, metadata=metadata)

        if response.code == grpc.StatusCode.OK.value[0]:
            return True

    except grpc.RpcError as e:
        print(f"check_transaction_risk - Code: {e.code()}")

        print(f"check_transaction_risk - Message: {e.details()}")

        return False
