import os
from typing import Optional

import grpc

from .protos import billing_details_pb2_grpc, billing_details_pb2

from .model import BillType

from .utils.billing_service_data_context import billing_service_data_context

def init_bwatch(auth_data: dict, middleware_data: dict):
    client_private_key = os.environ.get("BRIDGECARD_ISSUING_TLS_CLIENT_PRIVATE_KEY")

    client_certificate_chain = os.environ.get(
        "BRIDGECARD_ISSUING_TLS_CLIENT_CERT_CHAIN"
    )

    server_certificate_chain = os.environ.get(
        "BRIDGECARD_ISSUING_TLS_SERVER_CERT_CHAIN"
    )

    server_addr = "ae740cdf8e16b48bc82a259400ca03b9-1383199310.us-west-2.elb.amazonaws.com:80"

    creds = grpc.ssl_channel_credentials(
        private_key=client_private_key.encode(),
        certificate_chain=client_certificate_chain.encode(),
        root_certificates=server_certificate_chain.encode(),
    )

    grpc_channel = grpc.secure_channel(server_addr, creds)

    billing_service_data_context.grpc_channel = grpc_channel

