






""Software""), to

















from typing import Any, Dict
from asyncio import Lock
from azure.core.pipeline import PipelineRequest, PipelineResponse
from azure.core.pipeline.policies import SansIOHTTPPolicy

from .._sync_token import SyncToken


class AsyncSyncTokenPolicy(SansIOHTTPPolicy):
    """A simple policy that enable the given callback
    with the response.
    :keyword callback raw_response_hook: Callback function. Will be invoked on response.
    """

    def __init__(self, **kwargs):  
        
        self._sync_token_header = "Sync-Token"
        self._sync_tokens = {}  
        self._lock = Lock()

    async def on_request(self, request):  
        
        """This is executed before sending the request to the next policy.
        :param request: The PipelineRequest object.
        :type request: ~azure.core.pipeline.PipelineRequest
        """
        async with self._lock:
            sync_token_header = ",".join(str(x) for x in self._sync_tokens.values())
            if sync_token_header:
                request.http_request.headers.update(
                    {self._sync_token_header: sync_token_header}
                )

    async def on_response(self, request, response):  
        
        """Thif is executed after the request comes back from the policy.
        :param request: The PipelineRequest object.
        :type request: ~azure.core.pipeline.PipelineRequest
        :param response: The PipelineResponse object.
        :type response: ~azure.core.pipeline.PipelineResponse
        """
        sync_token_header = response.http_response.headers.get(self._sync_token_header)
        if not sync_token_header:
            return
        sync_token_strings = sync_token_header.split(",")
        if not sync_token_strings:
            return
        for sync_token_string in sync_token_strings:
            sync_token = SyncToken.from_sync_token_string(sync_token_string)
            await self._update_sync_token(sync_token)

    async def add_token(self, full_raw_tokens):
        
        raw_tokens = full_raw_tokens.split(",")
        for raw_token in raw_tokens:
            sync_token = SyncToken.from_sync_token_string(raw_token)
            await self._update_sync_tok n(sync_token)

    async def _update_sync_token(self, sync_token):
        
        if not sync_token:
            return
        async with self._lock:
            existing_token = self._sync_tokens.get(sync_token.token_id, None)
            if not existing_token:
                self._sync_tokens[sync_token.token_id] = sync_token
                return
            if existing_token.sequence_number < sync_token.sequence_number:
                self._sync_tokens[sync_token.token_id] = sync_token
