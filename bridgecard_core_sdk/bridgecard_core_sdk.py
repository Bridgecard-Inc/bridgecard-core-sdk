from typing import Optional
from .issuing.billing_service.billing_service import init_billing_service

def init(billing_service: Optional[bool] = False, billing_service_init_data:Optional[bool] = False):

    if billing_service:
        
        init_billing_service()



    







