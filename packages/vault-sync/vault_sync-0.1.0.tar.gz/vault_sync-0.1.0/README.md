# vault-sync #
[![Build Status](https://gitlab.com/solvinity/vault-sync/badges/main/pipeline.svg)](https://gitlab.com/solvinity/vault-sync/pipelines) [![Coverage Status](https://coveralls.io/repos/gitlab/solvinity/vault-sync/badge.svg?branch=HEAD)](https://coveralls.io/gitlab/solvinity/vault-sync?branch=HEAD)

## What is vault-sync? ##

`vault-sync` is a small command-line tool for copying (synchronizing) secrets from one Hashicorp Vault instance or another.

This can useful either for backup reasons or for ensuring that changes in one environment are correctly brought over to the other.

## Using vault-sync and config file ##

Vault-sync is a command-line tool that by default uses a small JSON document file to connect to the vault instances.

Any file can be used by the tool by using the `--config=<path to file>` flag. Do note however that [`pydantic`](https://pydantic-docs.helpmanual.io/) is used to strictly
enforce the layout of the JSON document.

The configuration document should look like this:

```json
{
    "source": {
        "url": "https://test1.com",
        "role_id": "da4f99bf-063e-4025-929b-0500a5bb145b",
        "secret_id": "2771dba9-f17b-4409-9e34-ef0f8efc9b61",
        "kv_store": "store1"
    },
    "destination": {
        "url": "https://test2.com",
        "role_id": "8d900c30-e078-4981-a1be-01c2a0770f2b",
        "secret_id": "d1c5468e-15ee-427f-b69d-b77d214b2bfd",
        "kv_store": "store2"
    }
}
```
