import src.utils.constants as constants
import json
from starlette.requests import Request
from starlette.responses import JSONResponse
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class InvalidToken(Exception):
    pass


class AuthenticationTokenMismatch(Exception):
    pass


class IssuingPermissionHasBeenDeactivated(Exception):
    pass


async def invalid_token_exception_handler(
    request: Request = None, exception: InvalidToken = None
):
    return JSONResponse(
        status_code=401,
        content={"message": "Not authenticated, Invalid Token", "status": False},
    )


async def live_authentication_token_for_sandbox_exception_handler(
    request: Request = None, exception: AuthenticationTokenMismatch = None
):
    return JSONResponse(
        status_code=401,
        content={
            "message": "Authentication error you are using a sandbox key in a live environment.",
            "status": False,
        },
    )


async def issuing_permission_deactivated_exception_handler(
    request: Request = None, exception: IssuingPermissionHasBeenDeactivated = None
):
    return JSONResponse(
        status_code=403,
        content={
            "message": "Your issuing permissions has been deactivated, please contact support",
            "status": False,
        },
    )


exception_handlers = {
    InvalidToken: invalid_token_exception_handler,
    IssuingPermissionHasBeenDeactivated: issuing_permission_deactivated_exception_handler,
    AuthenticationTokenMismatch: live_authentication_token_for_sandbox_exception_handler,
}


async def parse_error(exception_class):
    if type(exception_class) == dict:
        return {
            "status_code": exception_class["status_code"],
            "message": {"message": exception_class["message"]},
        }
    else:
        value = exception_handlers.get(exception_class)

        if not value:
            return {
                "status_code": 400,
                "message": "We ran into an error running this operation, please try again.",
            }

        val = await value()
        body = val.body
        body = json.loads(body.decode("UTF-8"))
        return {"status_code": val.status_code, "message": body}


async def parse_kyc_error(exception_class):
    if "data" in list(exception_class.keys()):
        return JSONResponse(
            status_code=400,
            content={
                "message": exception_class["message"],
                "data": exception_class["data"],
            },
        )
    else:
        return JSONResponse(
            status_code=400, content={"message": exception_class["message"]}
        )


def generate_kyc_error(status_code: int, message: str):
    return {"status_code": status_code, "message": message}


def generate_cardholder_error(status_code: int, message: str, data: str):
    return {"status_code": status_code, "message": message, "data": data}


IDNoDoesntMatchID_error_description = {
    "error_description": "Oops.. The uploaded ID number doesn't match the ID uploaded, please try again."
}
InvalidID_error_description = {
    "error_description": "Oops.. We couldn't verify this ID, please confirm that the ID is not expired and that it's properly snapped with the four edges showing, we do not accept scans but only live images."
}
NameDoesntMatchID_error_description = {
    "error_description": "Oops.. The uploaded ID details doesn't match the name on the cardholder profile, please try again."
}
CouldntVerifyID_error_description = {
    "error_description": "Oops.. we're having issues verifying your ID at the moment, it's our fault not yours, the Government ID provider for this service is currently down. Please try again after some time, or try using another ID type.."
}
SelfieImageDoesntMatch_error_description = {
    "error_description": "Oops.. The selfie image doesn't match the image on the uploaded ID. Please try taking another selfie and this time please remove any eye glasses or face caps."
}
InvalidImage_error_description = {
    "error_description": "Oops.. We couldn't use the selfie image you uploaded, please try taking another selfie and this time the image is clear, remove any eye glasses or face caps."
}
InvalidImag2_error_description = {
    "error_description": "Oops.. We couldn't use the selfie image you uploaded, please make sure that the image you take is close up to your face as much as possible without showing so many background."
}
IDDetailsDoesntMatchProvidedInformation_error_description = {
    "error_description": "Oops.. The uploaded ID details doesn't match the profile details of this cardholder, please try again."
}
BlacklistedBVNProfile_error_description = {
    "error_description": "Oops.. your BVN might have been associated with some fraud or bad record recently so we couldn't enroll you. please contact your bank."
}
WeCouldntVerifyBVN_error_description = {
    "error_description": "Oops.. we couldn't verify your BVN, please confirm the BVN and try again."
}
BVNNameDoesntMatchID_error_description = {
    "error_description": "Oops.. The uploaded ID name doesn't match the name on his BVN, please try again."
}
NameDoesntMatchID_error_description = {
    "error_description": "Oops.. The uploaded ID name doesn't match the name on his Cardholder, please try again."
}
NameDoesntMatchID_error_description = {
    "error_description": "Oops.. The uploaded ID name doesn't match the name on his Cardholder, please try again."
}
cardholder_PEP_sanction_error_description = {
    "error_description": "Oops.. This cardholder is either on the PEP, Sanction or Criminal list."
}
couldnt_verify_cardholder_error_description = {
    "error_description": "Oops.. we couldn't verify cardholders PEP, Sanction or Criminal status, please and try again."
}
