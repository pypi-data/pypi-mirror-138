from ._client import (browser_authenticate, decrypt_msg,
                      poll_opaque_token_service)
from ._crypto import generate_keys


class TokenMessage:
    def __init__(self, access_token, sidecar_endpoints, user_email) -> None:
        self.access_token = access_token
        self.sidecar_endpoints = sidecar_endpoints
        self.user_email = user_email


def retrieve_token(address, idp, silent, timeout):
    private_key, public_key = generate_keys()
    browser_authenticate(address, public_key, silent, idp=idp)
    msg = poll_opaque_token_service(address, public_key, timeout)
    decrypt_msg(msg, private_key)
    # note: despite the field name, this access token is not encrypted anymore.
    # it was decrypted by the above line
    return TokenMessage(
        access_token=msg["EncryptedAccessToken"],
        sidecar_endpoints=msg.get("SidecarEndpoints"),
        user_email=msg.get("UserEmail"),
    )
