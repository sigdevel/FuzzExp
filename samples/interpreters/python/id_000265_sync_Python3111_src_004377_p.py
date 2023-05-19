







"""
FILE: file_samples_share_async.py

DESCRIPTION:
    These samples demonstrate share operations like creating a share snapshot,
    setting share quota and metadata, listing directories and files in the
    file share, and getting directory and file clients from a share client.

USAGE:
    python file_samples_share_async.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_STORAGE_CONNECTION_STRING - the connection string to your storage account
"""

import os
import asyncio
from azure.storage.fileshare import ShareAccessTier

SOURCE_FILE = './SampleSource.txt'
DEST_FILE = './SampleDestination.txt'


class ShareSamplesAsync(object):

    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    async def create_share_snapshot_async(self):
        
        from azure.storage.fileshare.aio import ShareClient
        share = ShareClient.from_connection_string(self.connection_string, "sharesamples1")

        async with share:
            
            
            await share.create_share(access_tier=ShareAccessTier("Hot"))
            
            try:
                
                await share.create_snapshot()
                
            finally:
                
                await share.delete_share(delete_snapshots=True)
                

    async def set_share_quota_and_metadata_async(self):
        
        from azure.storage.fileshare.aio import ShareClient
        share = ShareClient.from_connection_string(self.connection_string, "sharesamples2")
        

        
        async with share:
            await share.create_share()

            try:
                
                
                await share.set_share_quota(quota=1)
                

                
                data = {'category': 'test'}
                await share.set_share_metadata(metadata=data)
                

                
                props = (await share.get_share_properties()).metadata

            finally:
                
                await share.delete_share()

    async def set_share_properties(self):
        from azure.storage.fileshare.aio import ShareClient
        share1 = ShareClient.from_connection_string(self.connection_string, "sharesamples3a")
        share2 = ShareClient.from_connection_string(self.connection_string, "sharesamples3b")

        
        async with share1 and share2:
            await share1.create_share()
            await share2.create_share()

            try:
                
                
                await share1.set_share_properties(access_tier="Hot")
                
                await share1.set_share_properties(quota=3)
                
                await share2.set_share_properties(access_tier=ShareAccessTier("Cool"), quota=2)

                
                props1 = await share1.get_share_properties()
                props2 = await share2.get_share_properties()
                print(props1.access_tier)
                print(props1.quota)
                print(props2.access_tier)
                print(props2.quota)
                

            finally:
                
                await share1.delete_share()
                await share2.delete_share()

    async def list_directories_and_files_async(self):
        
        from azure.storage.fileshare.aio import ShareClient
        share = ShareClient.from_connection_string(self.connection_string, "sharesamples4")

        
        async with share:
            await share.create_share()

            try:
                
                
                dir_client = await share.create_directory("mydir")

                
                with open(SOURCE_FILE, "rb") as source_file:
                    await dir_client.upload_file(file_name="sample", data=source_file)

                
                my_files = []
                async for item in share.list_directories_and_files(directory_name="mydir"):
                    my_files.append(item)
                print(my_files)
                
            finally:
                
                await share.delete_share()

    async def get_directory_or_file_client_async(self):
        
        from azure.storage.fileshare.aio import ShareClient
        share = ShareClient.from_connection_string(self.connection_string, "sharesamples5")

        
        my_dir = share.get_directory_client("dir1")

        
        my_file = share.get_file_client("dir1/myfile")


async def main():
    sample = ShareSamplesAsync()
    await sample.create_share_snapshot_async()
    await sample.set_share_quota_and_metadata_async()
    await sample.set_share_properties()
    await sample.list_directories_and_files_async()
    await sample.get_directory_or_file_client_async()

if __name__ == '__main__':
    asyncio.run(main())
