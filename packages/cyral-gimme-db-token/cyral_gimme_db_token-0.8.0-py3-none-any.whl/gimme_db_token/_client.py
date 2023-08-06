import json
import logging
import time
import webbrowser
from pathlib import Path

import requests

from ._crypto import decrypt

logger = logging.getLogger("gimme_db_token")


def browser_authenticate(address, public_key, silent, idp=None):
    url = f"https://{address}/app/cli/{public_key}"
    if idp is not None:
        url += f"?idp={idp}"
    webbrowser.open(url)
    if not silent:
        print("Please continue the authentication in the opened browser window.")
        print(
            "If the window didn't automatically start, please open the following URL in your browser:"
        )
        print(url)
        print("")


def poll_opaque_token_service(address, public_key, timeout):
    time_before_retry = 1  # in seconds
    num_tries = int(timeout / time_before_retry)
    if num_tries == 0:
        num_tries = 1
    url = f"https://{address}:8000/v1/opaqueToken/tokens/{public_key}"
    for _ in range(num_tries):
        try:
            r = requests.get(url)
            logger.debug(r)
            logger.debug(r.text)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            continue
        if r.status_code == 200:
            # successful, return
            return json.loads(r.text)
        time.sleep(time_before_retry)
    # if here, then timed out
    raise requests.exceptions.Timeout(
        f"Timeout error. Latest response from server is {r.status_code}:{r.text}"
    )


def decrypt_msg(msg, private_key):
    # note: everything in this message is encrypted, not just the
    # "EncryptedAccessToken" field. Ideally, we would have named it
    if "EncryptedAccessToken" in msg:
        msg["EncryptedAccessToken"] = decrypt(msg["EncryptedAccessToken"], private_key)
    if "SidecarEndpoints" in msg:
        sidecars = [decrypt(m, private_key) for m in msg["SidecarEndpoints"]]
        msg["SidecarEndpoints"] = sidecars
    if "UserEmail" in msg:
        msg["UserEmail"] = decrypt(msg["UserEmail"], private_key)


def get_cyral_ca_bundle(cyral_address, direname):
    ca_bundle_default_path = Path(direname) / "cyral_ca_bundle.pem"
    if ca_bundle_default_path.is_file():
        return str(ca_bundle_default_path)
    ca_bundle_url = f"https://{cyral_address}:8000/v1/templates/ca_bundle"
    ca_bundle = requests.get(ca_bundle_url)
    ca_bundle.raise_for_status()
    with open(ca_bundle_default_path, "w") as f:
        f.write(ca_bundle.text)
    return str(ca_bundle_default_path)
