# Bridgecard Core SDK - This library helps us centralize communication to our services through one package.

## How to Integrate:

### 1. Installation

pip install git+https://github.com/Bridgecard-Inc/bridgecard-core-sdk.git#egg=bridgecard-core-sdk

### 2. Initialization

```python

from bridgecard_core_sdk import bridgecard_core_sdk
from bridgecard_core_sdk.issuing.billing_service import billing_service
from bridgecard_core_sdk.issuing.billing_service.model import BillType

bridgecard_core_sdk.init(billing_service=True)
```

### 3. Rewards Billing sample

```python

admin_token = ""

amount_left = billing_service.check_admin_bill_status(token=admin_token,bill_type=BillType.CARD_REWARDS_FEE)

print(amount_left)

admin_billed = billing_service.bill_admin(token=admin_token,bill_type=BillType.CARD_REWARDS_FEE)

print(admin_billed)

```

### 4. NGN Cards Billing sample

```python

admin_token = ""

amount_left = billing_service.check_admin_bill_status(token=admin_token,bill_type=BillType.CARD_ISSUING_FEE_NGN_VIRTUAL_CARD)

print(amount_left)

admin_billed = billing_service.bill_admin(token=admin_token,bill_type=BillType.CARD_ISSUING_FEE_NGN_VIRTUAL_CARD)

print(admin_billed)

admin_billed = billing_service.bill_admin(token=admin_token,bill_type=BillType.CARD_ISSUING_FEE_NGN_VIRTUAL_CARD)

print(admin_billed)

```