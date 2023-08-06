import logging
import sys
from urllib.parse import urlparse

import click

from ._aws import (configure_s3_proxy_settings, s3_proxy_is_configured,
                   update_aws_creds, update_s3_proxy_endpoint)
from ._pgpass import update_pgpass
from ._token import retrieve_token

logger = logging.getLogger("gimme_db_token")


@click.command(name="gimme_db_token")
@click.argument("db", type=click.Choice(["pg", "s3"], case_sensitive=False), nargs=-1)
@click.option(
    "--address",
    required=False,
    envvar="CYRAL_ADDRESS",
    show_envvar=True,
    help="Address (FQDN) of Cyral controlplane. Example: acme.cyral.com.",
)
@click.option(
    "--tenant",
    required=False,
    envvar="CYRAL_TENANT",
    show_envvar=True,
    help="Tenant Name. If given, the controlplane address will be assumed to be <tenant>.cyral.com",
)
@click.option(
    "--sidecar",
    required=False,
    envvar="CYRAL_SIDECAR",
    show_envvar=True,
    help="(Required only for S3) Sidecar endpoint. Required to autoconfigure S3 proxy settings. Example: sidecar.endpoint.com:453 where `453` is the sidecar listener port assigned to the S3 repo",
)
@click.option(
    "--autoconfigure/--no-autoconfigure",
    required=False,
    default=None,
    help="(Required only for S3) Enable/Disable S3 proxy settings autoconfiguration and prompts. If omitted, user input will be required if S3 proxy is misconfigured.",
)
@click.option(
    "--profile",
    help="(Required only for S3) Name of AWS profile to store S3 access credentials in. NOTE: any existing credentials in this profile will be overwritten. If no AWS profile with the provided name exists, it will be created.",
)
@click.option(
    "--stdout",
    help="Print the access token to stdout. The token will not be stored in the specified credential files.",
    is_flag=True,
)
@click.option("--silent", help="Run the program quietly.", is_flag=True)
@click.option(
    "--idp",
    required=False,
    envvar="CYRAL_IDP",
    show_envvar=True,
    help="If not logged in, you will be redirected to the IdP with this ID.",
)
@click.option(
    "--timeout",
    default=5 * 60,
    envvar="CYRAL_DB_TOKEN_TIMEOUT",
    type=click.INT,
    show_envvar=True,
    help="Number of seconds to wait for Cyral server to respond before timeout",
)
@click.option("-v", "--verbose", is_flag=True)
@click.version_option(version="0.8.0")
def update_token(
    db,
    address,
    tenant,
    sidecar,
    autoconfigure,
    profile,
    stdout,
    silent,
    idp,
    timeout,
    verbose,
):
    """Fetch a fresh database access token from Cyral and store it locally.
    Currently, gimme_db_token supports Postgresql and S3 (with more coming!).
    If a database type is not specified, Postgresql database type is used.

    Example usage:

        This command will fetch a database access token for Postgresql and store it in your system.

        > gimme_db_token pg --address mycompany.cyral.com

        This is equivalent to:

        > gimme_db_token pg --tenant mycompany

        You can also specify multiple database types:

        > gimme_db_token pg s3 --address mycompany.cyral.com --profile myprofile

        To store database access token in an environment variable with one command, run the following:

        > export CYRAL_TOKEN=$(gimme_db_token --address mycompany.cyral.com --stdout --silent)

        To autoconfigure S3 proxy settings:

        > gimme_db_token s3 --autoconfigure --address mycompany.cyral.com --profile myprofile --sidecar sidecar.endpoint:453

        To silence S3 proxy misconfiguration prompts:

        > gimme_db_token s3 --no-autoconfigure --address mycompany.cyral.com --profile myprofile

    """
    # for backwards compatibility, if DB type is not set, use Postgresql
    db = db or ("pg",)
    if not (bool(tenant) ^ bool(address)):
        print(
            "Please provide either a Cyral controlplane address via --address or a tenant name via --tenant."
        )
        sys.exit(1)
    address = address or f"{tenant}.cyral.com"
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("/* IN DEBUG MODE */")
    try:
        if stdout:
            stdout_handler(address, idp, silent, timeout)
        else:
            if "pg" in db:
                pg_handler(address, idp, silent, timeout)
            if "s3" in db:
                s3_handler(address, idp, silent, timeout, profile, sidecar, autoconfigure)

    except Exception as e:
        print(
            "There was an error fetching your token. If this persists, please run the tool with the -v flag and contact support@cyral.com with the output. We’d be happy to help!"
        )
        if verbose:
            raise e


def stdout_handler(address, idp, silent, timeout):
    msg = retrieve_token(address, idp, silent, timeout)
    print(msg.access_token)


def pg_handler(address, idp, silent, timeout):
    msg = retrieve_token(address, idp, silent, timeout)
    update_pgpass(msg.access_token, msg.sidecar_endpoints, silent)


def s3_handler(address, idp, silent, timeout, profile, sidecar, autoconfigure):
    if not profile:
        print("Please provide an AWS profile name to use via --profile")
        sys.exit(1)
    # check and configure s3 proxy settings
    if not s3_proxy_is_configured(profile):
        user_input = ""
        if autoconfigure is None:
            user_input = input(
                "S3 proxy settings are not correctly configured to work with Cyral. "
                "Proceed with the configuration first? [y/n] "
            )
        if autoconfigure or str(user_input) == "y":
            check_sidecar_arg(sidecar)
            configure_s3_proxy_settings(profile, sidecar, address)
            if not silent:
                print("Successfully configured S3 proxy settings.")
    elif sidecar:
        # the tool is configured but need to update the sidecar address
        check_sidecar_arg(sidecar)
        update_s3_proxy_endpoint(profile, sidecar)
    # update aws creds with access token
    msg = retrieve_token(address, idp, silent, timeout)
    update_aws_creds(
        msg.access_token,
        msg.user_email,
        profile,
        silent,
    )


def check_sidecar_arg(sidecar):
    if not sidecar:
        # sidecar endpoint is required
        print(
            "Please provide a Cyral sidecar address to configure S3 proxy settings via --sidecar."
        )
        sys.exit(1)
    if not (urlparse(sidecar).port or urlparse("http://" + sidecar).port):
        # no port was specified in the sidecar endpoint
        print(
            "Please specify the listener port for S3 in your sidecar endpoint as well (e.g. 'sidecar.endpoint:453')."
        )
        sys.exit(1)


def run():
    update_token(prog_name="gimme_db_token")


if __name__ == "__main__":
    run()
