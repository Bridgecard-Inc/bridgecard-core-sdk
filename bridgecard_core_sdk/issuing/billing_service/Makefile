PROTO_DIR = ./bridgecard_core_sdk/issuing/billing_service/protos

cert:
	cd cert; ./gen.sh; cd ..

proto:
	ls
	rm -f $(PROTO_DIR)/*.py
	python3 -m grpc_tools.protoc -I $(PROTO_DIR) --python_out=$(PROTO_DIR) --grpc_python_out=$(PROTO_DIR) $(PROTO_DIR)/billing_details.proto

.PHONY: cert proto