#!/usr/bin/env python3
import json
from pathlib import Path
from typing import List, Union

import click
import hvac
from hvac.exceptions import InvalidRequest
from pydantic import ValidationError

from vault_sync.config import Config
from vault_sync.exceptions import ConfigException, VaultLoginException


class VaultSync:
    def __init__(self, config_file: str):
        self.config = self.load_config(config_file)
        self.source_client = hvac.Client(url=self.config.source.url)
        self.destination_client = hvac.Client(url=self.config.destination.url)
        self.authenticate_clients()

    @staticmethod
    def load_config(config_file: Union[Path, str]) -> Config:
        """Load a given configuration file into the pydantic structure

        Args:
            config_file (Union[Path, str]): Path to the config file

        Raises:
            ConfigException: If the file is incorrectly formatted or
            does not pass validation

        Returns:
            Config: Config object
        """
        try:
            with open(config_file) as json_file:
                data = json.load(json_file)
            config = Config(**data)
            return config
        except (json.JSONDecodeError, ValidationError) as err:
            raise ConfigException(str(err))

    def authenticate_clients(self) -> None:
        """Use the set configuration to authenticate to both the source
        and destination clients.

        Raises:
            VaultLoginException: Either of the clients returns an error.
        """
        try:
            self.source_client.auth.approle.login(
                role_id=self.config.source.role_id,
                secret_id=self.config.source.secret_id,
            )
            self.destination_client.auth.approle.login(
                role_id=self.config.destination.role_id,
                secret_id=self.config.destination.secret_id,
            )
        except InvalidRequest as err:
            raise VaultLoginException(str(err))

    def list_keys(self, kv_store_client: hvac.Client, kv_path: str) -> List[str]:
        """Return a list of the keys found at the given path

        Args:
            kv_store_client (hvac.Client): The vault client
            kv_path (str): Path inside the vault

        Returns:
            List[str]: A list of key names
        """
        list_response = kv_store_client.secrets.kv.v2.list_secrets(
            path=kv_path, mount_point=self.config.source.kv_store
        )
        return [key for key in list_response["data"]["keys"] if not key.endswith("/")]

    def list_folders(self, kv_store_client: hvac.Client, kv_path: str) -> List[str]:
        """Return a list of the folders found at the given path

        Args:
            kv_store_client (hvac.Client): The vault client
            kv_path (str): Path inside the vault

        Returns:
            List[str]: A list of folder names
        """
        list_response = kv_store_client.secrets.kv.v2.list_secrets(
            path=kv_path, mount_point=self.config.source.kv_store
        )
        return [key for key in list_response["data"]["keys"] if key.endswith("/")]

    def list_all_paths_in_source(self) -> List[str]:
        """Return a list of paths in the source client, starting from the root

        Returns:
            List[str]: List of vault paths
        """
        return self.walk_paths(self.source_client, "", [""])

    def walk_paths(self, client: hvac.Client, root: str, folders: List[str]) -> List[str]:
        """Recursively walk from a given root and return a list of the discovered paths

        Args:
            client (hvac.Client): Vault client
            root (str): Starting path
            folders (List[str]): List of found vault paths

        Returns:
            List[str]: List of vault paths
        """
        paths = [f"{root}{folder}" for folder in self.list_folders(client, root)]
        folders.extend(paths)
        for folder in paths:
            self.walk_paths(client, folder, folders)
        return folders

    def list_all_keys_in_source(self) -> List[str]:
        """Return a list of all the keys in the source client

        Returns:
            List[str]: List of keys
        """
        return [
            f"{explore}{key}"
            for explore in self.list_all_paths_in_source()
            for key in self.list_keys(self.source_client, explore)
        ]

    def get_secret_from_source(self, secret_path: str) -> dict:
        """Retrieve a secret from the source client using the path

        Args:
            secret_path (str): Path pointing to the secret

        Returns:
            dict: Secret data
        """
        secret_version_response = self.source_client.secrets.kv.v2.read_secret_version(
            path=secret_path,
            mount_point=self.config.source.kv_store
        )
        return secret_version_response["data"]["data"]

    def update_destination_secret(self, secret_path: str, secret_data: dict) -> None:
        """Update a secret at the destination at the given path using
        the given data.

        Args:
            secret_path (str): Path pointing to the secret
            secret_data (dict): Secret data
        """
        self.destination_client.secrets.kv.v2.create_or_update_secret(
            path=secret_path,
            mount_point=self.config.destination.kv_store,
            secret=secret_data
        )

    def sync(self, secret_path: str) -> None:
        """Sync a single secret from the source to the destination.

        Args:
            secret_path (str): Complete path to secret to sync
        """
        self.update_destination_secret(secret_path, self.get_secret_from_source(secret_path))

    def sync_all(self) -> None:
        """Run through the entire source and sync all keys to the destination.
        """
        for secret_path in self.list_all_keys_in_source():
            print(f"update secret: {secret_path}")
            self.sync(secret_path)
        print("all updates done.")


@click.command()
@click.option(
    "--config",
    default="config.json",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Path to the configuration file"
)
@click.option("--only-list-keys", is_flag=True, help="Only list the secret keys in the source")
def main(config, only_list_keys):
    click.echo(f"Current value is: {only_list_keys}")
    try:
        vault_sync = VaultSync(config_file=config)
        if only_list_keys:
            keys = "\n".join(vault_sync.list_all_keys_in_source())
            click.echo(f"Secret keys in source:\n{keys}")
        else:
            vault_sync.sync_all()
    except (ConfigException, VaultLoginException) as err:
        click.echo(str(err))


if __name__ == "__main__":
    main()
