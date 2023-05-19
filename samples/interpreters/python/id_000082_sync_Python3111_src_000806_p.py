



import asyncio


import pytest
from devtools_testutils import AzureRecordedTestCase, is_live
from devtools_testutils.aio import recorded_by_proxy_async
from devtools_testutils.sanitizers import set_custom_default_matcher

from _async_test_case import AsyncSecretsClientPreparer
from _shared.test_case_async import KeyVaultTestCase
from _test_case import get_decorator

all_api_versions = get_decorator()


def print(*args):
    assert all(arg is not None for arg in args)


@pytest.mark.asyncio
async def test_create_secret_client():
    vault_url = "vault_url"
    
    
    from azure.identity.aio import DefaultAzureCredential
    from azure.keyvault.secrets.aio import SecretClient

    
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url, credential)

    
    
    await secret_client.close()
    await credential.close()
    


class TestExamplesKeyVault(KeyVaultTestCase):
    @AzureRecordedTestCase.await_prepared_test
    @pytest.mark.parametrize("api_version", all_api_versions, ids=all_api_versions)
    @AsyncSecretsClientPreparer()
    @recorded_by_proxy_async
    async def test_example_secret_crud_operations(self, client, **kwargs):
        secret_client = client
        secret_name = self.get_resource_name("secret-name")

        
        from dateutil import parser as date_parse

        expires_on = date_parse.parse("2050-02-02T08:00:00.000Z")
        async with secret_client:
            
            secret = await secret_client.set_secret(secret_name, "secret-value", enabled=True, expires_on=expires_on)

            print(secret.id)
            print(secret.name)
            print(secret.properties.enabled)
            print(secret.properties.expires_on)
            

            secret_version = secret.properties.version
            
            
            secret = await secret_client.get_secret(secret_name)

            
            secret = await secret_client.get_secret(secret_name, secret_version)

            print(secret.id)
            print(secret.name)
            print(secret.properties.version)
            print(secret.properties.vault_url)
            

            
            
            content_type = "text/plain"
            tags = {"foo": "updated tag"}
            updated_secret_properties = await secret_client.update_secret_properties(
                secret_name, content_type=content_type, tags=tags
            )

            print(updated_secret_properties.version)
            print(updated_secret_properties.updated_on)
            print(updated_secret_properties.content_type)
            print(updated_secret_properties.tags)
            

            
            
            deleted_secret = await secret_client.delete_secret(secret_name)

            print(deleted_secret.name)

            
            
            print(deleted_secret.deleted_date)
            print(deleted_secret.scheduled_purge_date)
            print(deleted_secret.recovery_id)
            

    @AzureRecordedTestCase.await_prepared_test
    @pytest.mark.parametrize("api_version", all_api_versions, ids=all_api_versions)
    @AsyncSecretsClientPreparer()
    @recorded_by_proxy_async
    async def test_example_secret_list_operations(self, client, **kwargs):
        if not is_live():
            set_custom_default_matcher(excluded_headers="Authorization")
        secret_client = client
        async with secret_client:
            for i in range(7):
                secret_name = self.get_resource_name("secret{}".format(i))
                await secret_client.set_secret(secret_name, "value{}".format(i))

            
            
            secrets = secret_client.list_properties_of_secrets()

            async for secret in secrets:
                
                print(secret.id)
                print(secret.name)
                print(secret.enabled)
            

            
            
            secret_versions = secret_client.list_properties_of_secret_versions("secret-name")

            async for secret in secret_versions:
                
                print(secret.id)
                print(secret.enabled)
                print(secret.updated_on)
            

            
            
            deleted_secrets = secret_client.list_deleted_secrets()

            async for secret in deleted_secrets:
                
                print(secret.id)
                print(secret.name)
                print(secret.scheduled_purge_date)
                print(secret.recovery_id)
                print(secret.deleted_date)
            

    @AzureRecordedTestCase.await_prepared_test
    @pytest.mark.parametrize("api_version", all_api_versions, ids=all_api_versions)
    @AsyncSecretsClientPreparer()
    @recorded_by_proxy_async
    async def test_example_secrets_backup_restore(self, client, **kwargs):
        secret_client = client
        secret_name = self.get_resource_name("secret-name")
        async with secret_client:
            await secret_client.set_secret(secret_name, "secret-value")
            
            
            secret_backup = await secret_client.backup_secret(secret_name)

            
            print(secret_backup)
            

            await secret_client.delete_secret(secret_name)
            await secret_client.purge_deleted_secret(secret_name)

            if self.is_live:
                await asyncio.sleep(60)

            
            
            restored_secret = await secret_client.restore_secret_backup(secret_backup)
            print(restored_secret.id)
            print(restored_secret.version)
            

    @AzureRecordedTestCase.await_prepared_test
    @pytest.mark.parametrize("api_version", all_api_versions, ids=all_api_versions)
    @AsyncSecretsClientPreparer()
    @recorded_by_proxy_async
    async def test_example_secrets_recover(self, client, **kwargs):
        secret_client = client
        secret_name = self.get_resource_name("secret-name")
        async with client:
            await secret_client.set_secret(secret_name, "secret-value")
            await secret_client.delete_secret(secret_name)

            
            
            deleted_secret = await secret_client.get_deleted_secret(secret_name)
            print(deleted_secret.name)
            

            
            
            recovered_secret = await secret_client.recover_deleted_secret(secret_name)
            print(recovered_secret.id)
            print(recovered_secret.name)
            
