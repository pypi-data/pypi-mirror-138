import os
import subprocess
import sys
from pathlib import Path

import pkg_resources
import yaml
from awscli.customizations.configure.writer import ConfigFileWriter
from botocore.session import get_session

from ._client import get_cyral_ca_bundle

S3_PROXY_PLUGIN = "awscli-plugin-s3-proxy"


def get_config_file_path(file):
    # we use the botocore and awscli existing code to get this done.
    session = get_session()
    config_path = session.get_config_variable(file)
    config_path = os.path.expanduser(config_path)
    return config_path


def write_config_file(values, config_file_name):
    w = ConfigFileWriter()
    # this will create or update the profile as needed.
    w.update_config(values, config_file_name)


def update_aws_creds(access_token, user_email, aws_profile_name, silent):
    if not user_email:
        raise Exception("User email not returned from Cyral server")

    values = {
        "aws_access_key_id": f"{user_email}:{access_token}",
        "aws_secret_access_key": "none",
        "__section__": aws_profile_name,
    }

    creds_path = get_config_file_path("credentials_file")
    write_config_file(values, creds_path)

    if not silent:
        print(f"Updated S3 token for AWS profile '{aws_profile_name}' 🎉")
        if aws_profile_name != "default":
            print(
                "\nTo use this profile, specify the profile name using "
                "--profile, as shown:\n\n"
                f"aws s3 ls --profile {aws_profile_name}\n"
            )


def configure_s3_proxy_settings(aws_profile_name, sidecar_endpoint, cyral_address):
    try:
        if not s3_plugin_is_installed():
            install_s3_proxy_plugin()
        update_s3_proxy_plugins()
        update_ca_bundle(aws_profile_name, cyral_address)
        update_s3_proxy_endpoint(aws_profile_name, sidecar_endpoint)
    except Exception as e:
        print(f"An error happened during S3 proxy settings configuration: {str(e)}")
        sys.exit(1)


def update_ca_bundle(aws_profile_name, cyral_address):
    config_path = get_config_file_path("config_file")
    ca_bundle_direname = os.path.dirname(config_path)
    cyral_ca_bundle_file = get_cyral_ca_bundle(cyral_address, ca_bundle_direname)
    values = {
        "ca_bundle": cyral_ca_bundle_file,
        "__section__": "profile " + aws_profile_name,
    }
    write_config_file(values, config_path)


def update_s3_proxy_plugins():
    installed_plugin_name = S3_PROXY_PLUGIN.replace("-", "_")
    values = {
        "s3-proxy": installed_plugin_name,
        "__section__": "plugins",
    }
    if get_cli_version() == "v2":
        values.update({"cli_legacy_plugin_path": get_cli_legacy_plugin_path()})
    config_path = get_config_file_path("config_file")
    write_config_file(values, config_path)


def update_s3_proxy_endpoint(aws_profile_name, sidecar_endpoint):
    sidecar_endpoint = sidecar_endpoint.replace("http://", "").replace("https://", "")
    values = {
        "s3": {
            "proxy": f"http://{sidecar_endpoint}",
        },
        "__section__": "profile " + aws_profile_name,
    }
    config_path = get_config_file_path("config_file")
    write_config_file(values, config_path)


def s3_proxy_is_configured(aws_profile_name):
    session = get_session()
    config = session.full_config
    # a correctly configured config looks like the following:
    # {
    #     "plugins":{
    #         "s3-proxy":"awscli_plugin_s3_proxy"
    #     },
    #     "profiles":{
    #         "cyral":{
    #             "ca_bundle":"/home/user/.aws/cyral_ca_bundle.pem",
    #             "s3":{
    #                 "proxy":"http://sidecar.endpoint:453"
    #             }
    #         }
    #     }
    # }
    return (
        # check if the config has a plugins field
        config.get("plugins")
        # check if plugins has an entry for "s3-proxy"
        and config["plugins"].get("s3-proxy")
        # check if the config has a "profiles" field
        and config.get("profiles")
        # check if an entry for the given aws profile exists inside "profiles"
        and config["profiles"].get(aws_profile_name)
        # check if "ca_bundle" got a value for the given aws profile
        and config["profiles"][aws_profile_name].get("ca_bundle")
        # check if the value given to "ca_bundle" is a valid file
        and Path(config["profiles"][aws_profile_name]["ca_bundle"]).is_file()
        # check if "s3" got a value for the given aws profile
        and config["profiles"][aws_profile_name].get("s3")
        # check if "proxy" got a non-None value inside that s3 object
        and config["profiles"][aws_profile_name]["s3"].get("proxy")
        # check if s3 proxy plugin is installed
        and s3_plugin_is_installed()
    )


def install_s3_proxy_plugin():
    # install plugin using pip
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", S3_PROXY_PLUGIN],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError:
        raise Exception("Failed to install S3 proxy plugin using pip.")


def get_cli_legacy_plugin_path():
    # should be the dir of the installed S3_PROXY_PLUGIN
    try:
        plugin_info = subprocess.check_output(
            [sys.executable, "-m", "pip", "show", S3_PROXY_PLUGIN],
        ).decode("utf-8")
        return yaml.safe_load(plugin_info)["Location"]
    except subprocess.CalledProcessError:
        raise Exception("Failed to find a legacy plugin path for AWS cli.")


def s3_plugin_is_installed():
    pkgs = [pkg.key for pkg in pkg_resources.working_set]
    return S3_PROXY_PLUGIN in pkgs


def get_cli_version():
    # returns the major version
    try:
        cli_output = subprocess.check_output(["aws", "--version"]).decode("utf-8")
        assert cli_output.startswith("aws-cli")
        # example output: aws-cli/2.1.15 Python/3.7.3 Linux/4.19.128 exe/x86_64.ubuntu.20 prompt/off
        aws_version = cli_output.split("/")[1]
        major_version = "v" + aws_version[0]
        return major_version
    except (subprocess.CalledProcessError, AssertionError):
        raise Exception(
            "Failed to get AWS cli version. Make sure AWS CLI is installed!"
        )
