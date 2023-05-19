

"ZigZag iterator."
import sys

if sys.version_info[0] >= 3:
    xrange = range

def move(x, y, columns, rows):
    "Tells us what to do next with x and y."
    if y < (rows - 1):
        return max(0, x-1), y+1
    return x+1, y

def zigzag(rows, columns):
    "ZigZag iterator, yields indices."
    x, y = 0, 0
    size = rows * columns
    for _ in xrange(size):
        yield y, x
        if (x + y) & 1:
            x, y = move(x, y, columns, rows)
        else:
            y, x = move(y, x, rows, columns)


i, row


"License");






"AS IS" BASIS,




import os


try:
    from unittest import mock
    from unittest.mock import AsyncMock  
except ImportError:  
    import mock

import math

from google.api_core import gapic_v1, grpc_helpers, grpc_helpers_async, path_template
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  
from google.protobuf import struct_pb2  
from google.type import latlng_pb2  
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.dialogflow_v2.services.participants import (
    ParticipantsAsyncClient,
    ParticipantsClient,
    pagers,
    transports,
)
from google.cloud.dialogflow_v2.types import audio_config, context, entity_type
from google.cloud.dialogflow_v2.types import participant
from google.cloud.dialogflow_v2.types import participant as gcd_participant
from google.cloud.dialogflow_v2.types import session, session_entity_type


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"





def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert ParticipantsClient._get_default_mtls_endpoint(None) is None
    assert (
        ParticipantsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        ParticipantsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ParticipantsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ParticipantsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert ParticipantsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (ParticipantsClient, "grpc"),
        (ParticipantsAsyncClient, "grpc_asyncio"),
    ],
)
def test_participants_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("dialogflow.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ParticipantsGrpcTransport, "grpc"),
        (transports.ParticipantsGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_participants_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (ParticipantsClient, "grpc"),
        (ParticipantsAsyncClient, "grpc_asyncio"),
    ],
)
def test_participants_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("dialogflow.googleapis.com:443")


def test_participants_client_get_transport_class():
    transport = ParticipantsClient.get_transport_class()
    available_transports = [
        transports.ParticipantsGrpcTransport,
    ]
    assert transport in available_transports

    transport = ParticipantsClient.get_transport_class("grpc")
    assert transport == transports.ParticipantsGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ParticipantsClient, transports.ParticipantsGrpcTransport, "grpc"),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ParticipantsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ParticipantsClient)
)
@mock.patch.object(
    ParticipantsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ParticipantsAsyncClient),
)
def test_participants_client_client_options(
    client_class, transport_class, transport_name
):
    
    with mock.patch.object(ParticipantsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    
    with mock.patch.object(ParticipantsClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    
    "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    
    "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    
    
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (ParticipantsClient, transports.ParticipantsGrpcTransport, "grpc", "true"),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ParticipantsClient, transports.ParticipantsGrpcTransport, "grpc", "false"),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ParticipantsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ParticipantsClient)
)
@mock.patch.object(
    ParticipantsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ParticipantsAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_participants_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    
    "true" and client cert exists.

    
    
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    
    
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [ParticipantsClient, ParticipantsAsyncClient])
@mock.patch.object(
    ParticipantsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(ParticipantsClient)
)
@mock.patch.object(
    ParticipantsAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ParticipantsAsyncClient),
)
def test_participants_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ParticipantsClient, transports.ParticipantsGrpcTransport, "grpc"),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_participants_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            ParticipantsClient,
            transports.ParticipantsGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_participants_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_participants_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dialogflow_v2.services.participants.transports.ParticipantsGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ParticipantsClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            ParticipantsClient,
            transports.ParticipantsGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ParticipantsAsyncClient,
            transports.ParticipantsGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_participants_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "dialogflow.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            scopes=None,
            default_host="dialogflow.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcd_participant.CreateParticipantRequest,
        dict,
    ],
)
def test_create_participant(request_type, transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        
        call.return_value = gcd_participant.Participant(
            name="name_value",
            role=gcd_participant.Participant.Role.HUMAN_AGENT,
            sip_recording_media_label="sip_recording_media_label_value",
            obfuscated_external_user_id="obfuscated_external_user_id_value",
        )
        response = client.create_participant(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.CreateParticipantRequest()

    
    assert isinstance(response, gcd_participant.Participant)
    assert response.name == "name_value"
    assert response.role == gcd_participant.Participant.Role.HUMAN_AGENT
    assert response.sip_recording_media_label == "sip_recording_media_label_value"
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


def test_create_participant_empty_call():
    
    
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        client.create_participant()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.CreateParticipantRequest()


@pytest.mark.asyncio
async def test_create_participant_async(
    transport: str = "grpc_asyncio",
    request_type=gcd_participant.CreateParticipantRequest,
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant(
                name="name_value",
                role=gcd_participant.Participant.Role.HUMAN_AGENT,
                sip_recording_media_label="sip_recording_media_label_value",
                obfuscated_external_user_id="obfuscated_external_user_id_value",
            )
        )
        response = await client.create_participant(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.CreateParticipantRequest()

    
    assert isinstance(response, gcd_participant.Participant)
    assert response.name == "name_value"
    assert response.role == gcd_participant.Participant.Role.HUMAN_AGENT
    assert response.sip_recording_media_label == "sip_recording_media_label_value"
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


@pytest.mark.asyncio
async def test_create_participant_async_from_dict():
    await test_create_participant_async(request_type=dict)


def test_create_participant_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = gcd_participant.CreateParticipantRequest()

    request.parent = "parent_value"

    
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        call.return_value = gcd_participant.Participant()
        client.create_participant(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_participant_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = gcd_participant.CreateParticipantRequest()

    request.parent = "parent_value"

    
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant()
        )
        await client.create_participant(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_participant_flattened():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        
        call.return_value = gcd_participant.Participant()
        
        
        client.create_participant(
            parent="parent_value",
            participant=gcd_participant.Participant(name="name_value"),
        )

        
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].participant
        mock_val = gcd_participant.Participant(name="name_value")
        assert arg == mock_val


def test_create_participant_flattened_error():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        client.create_participant(
            gcd_participant.CreateParticipantRequest(),
            parent="parent_value",
            participant=gcd_participant.Participant(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_participant_flattened_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(
        type(client.transport.create_participant), "__call__"
    ) as call:
        
        call.return_value = gcd_participant.Participant()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant()
        )
        
        
        response = await client.create_participant(
            parent="parent_value",
            participant=gcd_participant.Participant(name="name_value"),
        )

        
        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].participant
        mock_val = gcd_participant.Participant(name="name_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_participant_flattened_error_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        await client.create_participant(
            gcd_participant.CreateParticipantRequest(),
            parent="parent_value",
            participant=gcd_participant.Participant(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        participant.GetParticipantRequest,
        dict,
    ],
)
def test_get_participant(request_type, transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        
        call.return_value = participant.Participant(
            name="name_value",
            role=participant.Participant.Role.HUMAN_AGENT,
            sip_recording_media_label="sip_recording_media_label_value",
            obfuscated_external_user_id="obfuscated_external_user_id_value",
        )
        response = client.get_participant(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.GetParticipantRequest()

    
    assert isinstance(response, participant.Participant)
    assert response.name == "name_value"
    assert response.role == participant.Participant.Role.HUMAN_AGENT
    assert response.sip_recording_media_label == "sip_recording_media_label_value"
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


def test_get_participant_empty_call():
    
    
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        client.get_participant()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.GetParticipantRequest()


@pytest.mark.asyncio
async def test_get_participant_async(
    transport: str = "grpc_asyncio", request_type=participant.GetParticipantRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.Participant(
                name="name_value",
                role=participant.Participant.Role.HUMAN_AGENT,
                sip_recording_media_label="sip_recording_media_label_value",
                obfuscated_external_user_id="obfuscated_external_user_id_value",
            )
        )
        response = await client.get_participant(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.GetParticipantRequest()

    
    assert isinstance(response, participant.Participant)
    assert response.name == "name_value"
    assert response.role == participant.Participant.Role.HUMAN_AGENT
    assert response.sip_recording_media_label == "sip_recording_media_label_value"
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


@pytest.mark.asyncio
async def test_get_participant_async_from_dict():
    await test_get_participant_async(request_type=dict)


def test_get_participant_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = participant.GetParticipantRequest()

    request.name = "name_value"

    
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        call.return_value = participant.Participant()
        client.get_participant(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_participant_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = participant.GetParticipantRequest()

    request.name = "name_value"

    
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.Participant()
        )
        await client.get_participant(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_participant_flattened():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        
        call.return_value = participant.Participant()
        
        
        client.get_participant(
            name="name_value",
        )

        
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_participant_flattened_error():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        client.get_participant(
            participant.GetParticipantRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_participant_flattened_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(type(client.transport.get_participant), "__call__") as call:
        
        call.return_value = participant.Participant()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.Participant()
        )
        
        
        response = await client.get_participant(
            name="name_value",
        )

        
        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_participant_flattened_error_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        await client.get_participant(
            participant.GetParticipantRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        participant.ListParticipantsRequest,
        dict,
    ],
)
def test_list_participants(request_type, transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        
        call.return_value = participant.ListParticipantsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_participants(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.ListParticipantsRequest()

    
    assert isinstance(response, pagers.ListParticipantsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_participants_empty_call():
    
    
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        client.list_participants()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.ListParticipantsRequest()


@pytest.mark.asyncio
async def test_list_participants_async(
    transport: str = "grpc_asyncio", request_wype=participant.ListParticipantsRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.ListParticipantsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_participants(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.ListParticipantsRequest()

    
    assert isinstance(response, pagers.ListParticipantsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_participants_async_from_dict():
    await test_list_participants_async(request_type=dict)


def test_list_participants_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = participant.ListParticipantsRequest()

    request.parent = "parent_value"

    
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        call.return_value = participant.ListParticipantsResponse()
        client.list_participants(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_participants_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = participant.ListParticipantsRequest()

    request.parent = "parent_value"

    
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.ListParticipantsResponse()
        )
        await client.list_participants(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_participants_flattened():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        
        call.return_value = participant.ListParticipantsResponse()
        
        
        client.list_participants(
            parent="parent_value",
        )

        
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_participants_flattened_error():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        client.list_participants(
            participant.ListParticipantsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_participants_flattened_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        
        call.return_value = participant.ListParticipantsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.ListParticipantsResponse()
        )
        
        
        response = await client.list_participants(
            parent="parent_value",
        )

        
        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_participants_flattened_error_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        await client.list_participants(
            participant.ListParticipantsRequest(),
            parent="parent_value",
        )


def test_list_participants_pager(transport_name: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        
        call.side_effect = (
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                    participant.Participant(),
                ],
                next_page_token="abc",
            ),
            participant.ListParticipantsResponse(
                participants=[],
                next_page_token="def",
            ),
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                ],
                next_page_token="ghi",
            ),
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_participants(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, participant.Participant) for i in results)


def test_list_participants_pages(transport_name: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    
    with mock.patch.object(
        type(client.transport.list_participants), "__call__"
    ) as call:
        
        call.side_effect = (
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                    participant.Participant(),
                ],
                next_page_token="abc",
            ),
            participant.ListParticipantsResponse(
                participants=[],
                next_page_token="def",
            ),
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                ],
                next_page_token="ghi",
            ),
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_participants(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_participants_async_pager():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    
    with mock.patch.object(
        type(client.transport.list_participants),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        
        call.side_effect = (
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                    participant.Participant(),
                ],
                next_page_token="abc",
            ),
            participant.ListParticipantsResponse(
                participants=[],
                next_page_token="def",
            ),
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                ],
                next_page_token="ghi",
            ),
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_participants(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, participant.Participant) for i in responses)


@pytest.mark.asyncio
async def test_list_participants_async_pages():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    
    with mock.patch.object(
        type(client.transport.list_participants),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        
        call.side_effect = (
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                    participant.Participant(),
                ],
                next_page_token="abc",
            ),
            participant.ListParticipantsResponse(
                participants=[],
                next_page_token="def",
            ),
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                ],
                next_page_token="ghi",
            ),
            participant.ListParticipantsResponse(
                participants=[
                    participant.Participant(),
                    participant.Participant(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_participants(request={})
        ).pages:  
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        gcd_participant.UpdateParticipantRequest,
        dict,
    ],
)
def test_update_participant(request_type, transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        
        call.return_value = gcd_participant.Participant(
            name="name_value",
            role=gcd_participant.Participant.Role.HUMAN_AGENT,
            sip_recording_media_label="sip_recording_media_label_value",
            obfuscated_external_user_id="obfuscated_external_user_id_value",
        )
        response = client.update_participant(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.UpdateParticipantRequest()

    
    assert isinstance(response, gcd_participant.Participant)
    assert response.name == "name_value"
    assert response.role == gcd_participant.Participant.Role.HUMAN_AGENT
    assert response.sip_recording_media_label == "sip_recording_media_label_value"
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


def test_update_participant_empty_call():
    
    
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        client.update_participant()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.UpdateParticipantRequest()


@pytest.mark.asyncio
async def test_update_participant_async(
    transport: str = "grpc_asyncio",
    request_type=gcd_participant.UpdateParticipantRequest,
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant(
                name="name_value",
                role=gcd_participant.Participant.Role.HUMAN_AGENT,
                sip_recording_media_label="sip_recording_media_label_value",
                obfuscated_external_user_id="obfuscated_external_user_id_value",
            )
        )
        response = await client.update_participant(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.UpdateParticipantRequest()

    
    assert isinstance(response, gcd_participant.Participant)
    assert response.name == "name_value"
    assert response.role == gcd_participant.Participant.Role.HUMAN_AGENT
    assert response.sip_recording_media_label == "sip_recording_media_label_value"
    assert response.obfuscated_external_user_id == "obfuscated_external_user_id_value"


@pytest.mark.asyncio
async def test_update_participant_async_from_dict():
    await test_update_participant_async(request_type=dict)


def test_update_participant_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = gcd_participant.UpdateParticipantRequest()

    request.participant.name = "name_value"

    
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        call.return_value = gcd_participant.Participant()
        client.update_participant(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "participant.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_participant_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = gcd_participant.UpdateParticipantRequest()

    request.participant.name = "name_value"

    
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant()
        )
        await client.update_participant(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "participant.name=name_value",
    ) in kw["metadata"]


def test_update_participant_flattened():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        
        call.return_value = gcd_participant.Participant()
        
        
        client.update_participant(
            participant=gcd_participant.Participant(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].participant
        mock_val = gcd_participant.Participant(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_participant_flattened_error():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        client.update_participant(
            gcd_participant.UpdateParticipantRequest(),
            participant=gcd_participant.Participant(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_participant_flattened_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(
        type(client.transport.update_participant), "__call__"
    ) as call:
        
        call.return_value = gcd_participant.Participant()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.Participant()
        )
        
        
        response = await client.update_participant(
            participant=gcd_participant.Participant(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        
        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].participant
        mock_val = gcd_participant.Participant(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_participant_flattened_error_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        await client.update_participant(
            gcd_participant.UpdateParticipantRequest(),
            participant=gcd_participant.Participant(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        gcd_participant.AnalyzeContentRequest,
        dict,
    ],
)
def test_analyze_content(request_type, transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        
        call.return_value = gcd_participant.AnalyzeContentResponse(
            reply_text="reply_text_value",
        )
        response = client.analyze_content(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.AnalyzeContentRequest()

    
    assert isinstance(response, gcd_participant.AnalyzeContentResponse)
    assert response.reply_text == "reply_text_value"


def test_analyze_content_empty_call():
    
    
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        client.analyze_content()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.AnalyzeContentRequest()


@pytest.mark.asyncio
async def test_analyze_content_async(
    transport: str = "grpc_asyncio", request_type=gcd_participant.AnalyzeContentRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.AnalyzeContentResponse(
                reply_text="reply_text_value",
            )
        )
        response = await client.analyze_content(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gcd_participant.AnalyzeContentRequest()

    
    assert isinstance(response, gcd_participant.AnalyzeContentResponse)
    assert response.reply_text == "reply_text_value"


@pytest.mark.asyncio
async def test_analyze_content_async_from_dict():
    await test_analyze_content_async(request_type=dict)


def test_analyze_content_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = gcd_participant.AnalyzeContentRequest()

    request.participant = "participant_value"

    
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        call.return_value = gcd_participant.AnalyzeContentResponse()
        client.analyze_content(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "participant=participant_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_analyze_content_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = gcd_participant.AnalyzeContentRequest()

    request.participant = "participant_value"

    
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.AnalyzeContentResponse()
        )
        await client.analyze_content(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "participant=participant_value",
    ) in kw["metadata"]


def test_analyze_content_flattened():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        
        call.return_value = gcd_participant.AnalyzeContentResponse()
        
        
        client.analyze_content(
            participant="participant_value",
            text_input=session.TextInput(text="text_value"),
            event_input=session.EventInput(name="name_value"),
        )

        
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].participant
        mock_val = "participant_value"
        assert arg == mock_val
        assert args[0].event_input == session.EventInput(name="name_value")


def test_analyze_content_flattened_error():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        client.analyze_content(
            gcd_participant.AnalyzeContentRequest(),
            participant="participant_value",
            text_input=session.TextInput(text="text_value"),
            event_input=session.EventInput(name="name_value"),
        )


@pytest.mark.asyncio
async def test_analyze_content_flattened_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(type(client.transport.analyze_content), "__call__") as call:
        
        call.return_value = gcd_participant.AnalyzeContentResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcd_participant.AnalyzeContentResponse()
        )
        
        
        response = await client.analyze_content(
            participant="participant_value",
            text_input=session.TextInput(text="text_value"),
            event_input=session.EventInput(name="name_value"),
        )

        
        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].participant
        mock_val = "participant_value"
        assert arg == mock_val
        assert args[0].event_input == session.EventInput(name="name_value")


@pytest.mark.asyncio
async def test_analyze_content_flattened_error_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        await client.analyze_content(
            gcd_participant.AnalyzeContentRequest(),
            participant="participant_value",
            text_input=session.TextInput(text="text_value"),
            event_input=session.EventInput(name="name_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        participant.StreamingAnalyzeContentRequest,
        dict,
    ],
)
def test_streaming_analyze_content(request_type, transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()
    requests = [request]

    
    with mock.patch.object(
        type(client.transport.streaming_analyze_content), "__call__"
    ) as call:
        
        call.return_value = iter([participant.StreamingAnalyzeContentResponse()])
        response = client.streaming_analyze_content(iter(requests))

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    
    for message in response:
        assert isinstance(message, participant.StreamingAnalyzeContentResponse)


@pytest.mark.asyncio
async def test_streaming_analyze_content_async(
    transport: str = "grpc_asyncio",
    request_type=participant.StreamingAnalyzeContentRequest,
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()
    requests = [request]

    
    with mock.patch.object(
        type(client.transport.streaming_analyze_content), "__call__"
    ) as call:
        
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[participant.StreamingAnalyzeContentResponse()]
        )
        response = await client.streaming_analyze_content(iter(requests))

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    
    message = await response.read()
    assert isinstance(message, participant.StreamingAnalyzeContentResponse)


@pytest.mark.asyncio
async def test_streaming_analyze_content_async_from_dict():
    await test_streaming_analyze_content_async(request_type=dict)


@pytest.mark.parametrize(
    "request_type",
    [
        participant.SuggestArticlesRequest,
        dict,
    ],
)
def test_suggest_articles(request_type, transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        
        call.return_value = participant.SuggestArticlesResponse(
            latest_message="latest_message_value",
            context_size=1311,
        )
        response = client.suggest_articles(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestArticlesRequest()

    
    assert isinstance(response, participant.SuggestArticlesResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


def test_suggest_articles_empty_call():
    
    
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        client.suggest_articles()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestArticlesRequest()


@pytest.mark.asyncio
async def test_suggest_articles_async(
    transport: str = "grpc_asyncio", request_type=participant.SuggestArticlesRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestArticlesResponse(
                latest_message="latest_message_value",
                context_size=1311,
            )
        )
        response = await client.suggest_articles(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestArticlesRequest()

    
    assert isinstance(response, participant.SuggestArticlesResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


@pytest.mark.asyncio
async def test_suggest_articles_async_from_dict():
    await test_suggest_articles_async(request_type=dict)


def test_suggest_articles_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = participant.SuggestArticlesRequest()

    request.parent = "parent_value"

    
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        call.return_value = participant.SuggestArticlesResponse()
        client.suggest_articles(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_suggest_articles_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = participant.SuggestArticlesRequest()

    request.parent = "parent_value"

    
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestArticlesResponse()
        )
        await client.suggest_articles(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_suggest_articles_flattened():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        
        call.return_value = participant.SuggestArticlesResponse()
        
        
        client.suggest_articles(
            parent="parent_value",
        )

        
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_suggest_articles_flattened_error():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        client.suggest_articles(
            participant.SuggestArticlesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_suggest_articles_flattened_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(type(client.transport.suggest_articles), "__call__") as call:
        
        call.return_value = participant.SuggestArticlesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestArticlesResponse()
        )
        
        
        response = await client.suggest_articles(
            parent="parent_value",
        )

        
        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_suggest_articles_flattened_error_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        await client.suggest_articles(
            participant.SuggestArticlesRequest(),
            parent="parent_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        participant.SuggestFaqAnswersRequest,
        dict,
    ],
)
def test_suggest_faq_answers(request_type, transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        
        call.return_value = participant.SuggestFaqAnswersResponse(
            latest_message="latest_message_value",
            context_size=1311,
        )
        response = client.suggest_faq_answers(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestFaqAnswersRequest()

    
    assert isinstance(response, participant.SuggestFaqAnswersResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


def test_suggest_faq_answers_empty_call():
    
    
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        client.suggest_faq_answers()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestFaqAnswersRequest()


@pytest.mark.asyncio
async def test_suggest_faq_answers_async(
    transport: str = "grpc_asyncio", request_type=participant.SuggestFaqAnswersRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestFaqAnswersResponse(
                latest_message="latest_message_value",
                context_size=1311,
            )
        )
        response = await client.suggest_faq_answers(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestFaqAnswersRequest()

    
    assert isinstance(response, participant.SuggestFaqAnswersResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


@pytest.mark.asyncio
async def test_suggest_faq_answers_async_from_dict():
    await test_suggest_faq_answers_async(request_type=dict)


def test_suggest_faq_answers_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = participant.SuggestFaqAnswersRequest()

    request.parent = "parent_value"

    
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        call.return_value = participant.SuggestFaqAnswersResponse()
        client.suggest_faq_answers(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_suggest_faq_answers_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = participant.SuggestFaqAnswersRequest()

    request.parent = "parent_value"

    
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestFaqAnswersResponse()
        )
        await client.suggest_faq_answers(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_suggest_faq_answers_flattened():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        
        call.return_value = participant.SuggestFaqAnswersResponse()
        
        
        client.suggest_faq_answers(
            parent="parent_value",
        )

        
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_suggest_faq_answers_flattened_error():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        client.suggest_faq_answers(
            participant.SuggestFaqAnswersRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_suggest_faq_answers_flattened_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(
        type(client.transport.suggest_faq_answers), "__call__"
    ) as call:
        
        call.return_value = participant.SuggestFaqAnswersResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestFaqAnswersResponse()
        )
        
        
        response = await client.suggest_faq_answers(
            parent="parent_value",
        )

        
        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_suggest_faq_answers_flattened_error_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        await client.suggest_faq_answers(
            participant.SuggestFaqAnswersRequest(),
            parent="parent_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        participant.SuggestSmartRepliesRequest,
        dict,
    ],
)
def test_suggest_smart_replies(request_type, transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        
        call.return_value = participant.SuggestSmartRepliesResponse(
            latest_message="latest_message_value",
            context_size=1311,
        )
        response = client.suggest_smart_replies(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestSmartRepliesRequest()

    
    assert isinstance(response, participant.SuggestSmartRepliesResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


def test_suggest_smart_replies_empty_call():
    
    
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        client.suggest_smart_replies()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestSmartRepliesRequest()


@pytest.mark.asyncio
async def test_suggest_smart_replies_async(
    transport: str = "grpc_asyncio", request_type=participant.SuggestSmartRepliesRequest
):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = request_type()

    
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestSmartRepliesResponse(
                latest_message="latest_message_value",
                context_size=1311,
            )
        )
        response = await client.suggest_smart_replies(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == participant.SuggestSmartRepliesRequest()

    
    assert isinstance(response, participant.SuggestSmartRepliesResponse)
    assert response.latest_message == "latest_message_value"
    assert response.context_size == 1311


@pytest.mark.asyncio
async def test_suggest_smart_replies_async_from_dict():
    await test_suggest_smart_replies_async(request_type=dict)


def test_suggest_smart_replies_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = participant.SuggestSmartRepliesRequest()

    request.parent = "parent_value"

    
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        call.return_value = participant.SuggestSmartRepliesResponse()
        client.suggest_smart_replies(request)

        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_suggest_smart_replies_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = participant.SuggestSmartRepliesRequest()

    request.parent = "parent_value"

    
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestSmartRepliesResponse()
        )
        await client.suggest_smart_replies(request)

        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_suggest_smart_replies_flattened():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        
        call.return_value = participant.SuggestSmartRepliesResponse()
        
        
        client.suggest_smart_replies(
            parent="parent_value",
        )

        
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_suggest_smart_replies_flattened_error():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        client.suggest_smart_replies(
            participant.SuggestSmartRepliesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_suggest_smart_replies_flattened_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    with mock.patch.object(
        type(client.transport.suggest_smart_replies), "__call__"
    ) as call:
        
        call.return_value = participant.SuggestSmartRepliesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            participant.SuggestSmartRepliesResponse()
        )
        
        
        response = await client.suggest_smart_replies(
            parent="parent_value",
        )

        
        
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_suggest_smart_replies_flattened_error_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    with pytest.raises(ValueError):
        await client.suggest_smart_replies(
            participant.SuggestSmartRepliesRequest(),
            parent="parent_value",
        )


def test_credentials_transport_error():
    
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ParticipantsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ParticipantsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ParticipantsClient(
            client_options=options,
            transport=transport,
        )

    
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ParticipantsClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ParticipantsClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ParticipantsClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    
    transport = transports.ParticipantsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ParticipantsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ParticipantsGrpcTransport,
        transports.ParticipantsGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
    ],
)
def test_transport_kind(transport_name):
    transport = ParticipantsClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.ParticipantsGrpcTransport,
    )


def test_participants_base_transport_error():
    
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ParticipantsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_participants_base_transport():
    
    with mock.patch(
        "google.cloud.dialogflow_v2.services.participants.transports.ParticipantsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ParticipantsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    
    
    methods = (
        "create_participant",
        "get_participant",
        "list_participants",
        "update_participant",
        "analyze_content",
        "streaming_analyze_content",
        "suggest_articles",
        "suggest_faq_answers",
        "suggest_smart_replies",
        "get_location",
        "list_locations",
        "get_operation",
        "cancel_operation",
        "list_operations",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_participants_base_transport_with_credentials_file():
    
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dialogflow_v2.services.participants.transports.ParticipantsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ParticipantsTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


def test_participants_base_transport_with_adc():
    
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dialogflow_v2.services.participants.transports.ParticipantsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ParticipantsTransport()
        adc.assert_called_once()


def test_participants_auth_adc():
    
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ParticipantsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ParticipantsGrpcTransport,
        transports.ParticipantsGrpcAsyncIOTransport,
    ],
)
def test_participants_transport_auth_adc(transport_class):
    
    
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ParticipantsGrpcTransport,
        transports.ParticipantsGrpcAsyncIOTransport,
    ],
)
def test_participants_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.ParticipantsGrpcTransport, grpc_helpers),
        (transports.ParticipantsGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_participants_transport_create_channel(transport_class, grpc_helpers):
    
    
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "dialogflow.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/dialogflow",
            ),
            scopes=["1", "2"],
            default_host="dialogflow.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.ParticipantsGrpcTransport, transports.ParticipantsGrpcAsyncIOTransport],
)
def test_participants_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    
    
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_participants_host_no_port(transport_name):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("dialogflow.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_participants_host_with_port(transport_name):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dialogflow.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("dialogflow.googleapis.com:8000")


def test_participants_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    
    transport = transports.ParticipantsGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_participants_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    
    transport = transports.ParticipantsGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None




@pytest.mark.parametrize(
    "transport_class",
    [transports.ParticipantsGrpcTransport, transports.ParticipantsGrpcAsyncIOTransport],
)
def test_participants_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred




@pytest.mark.parametrize(
    "transport_class",
    [transports.ParticipantsGrpcTransport, transports.ParticipantsGrpcAsyncIOTransport],
)
def test_participants_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_answer_record_path():
    project = "squid"
    answer_record = "clam"
    expected = "projects/{project}/answerRecords/{answer_record}".format(
        project=project,
        answer_record=answer_record,
    )
    actual = ParticipantsClient.answer_record_path(project, answer_record)
    assert expected == actual


def test_parse_answer_record_path():
    expected = {
        "project": "whelk",
        "answer_record": "octopus",
    }
    path = ParticipantsClient.answer_record_path(**expected)

    
    actual = ParticipantsClient.parse_answer_record_path(path)
    assert expected == actual


def test_context_path():
    project = "oyster"
    session = "nudibranch"
    context = "cuttlefish"
    expected = "projects/{project}/agent/sessions/{session}/contexts/{context}".format(
        project=project,
        session=session,
        context=context,
    )
    actual = ParticipantsClient.context_path(project, session, context)
    assert expected == actual


def test_parse_context_path():
    expected = {
        "project": "mussel",
        "session": "winkle",
        "context": "nautilus",
    }
    path = ParticipantsClient.context_path(**expected)

    
    actual = ParticipantsClient.parse_context_path(path)
    assert expected == actual


def test_intent_path():
    project = "scallop"
    intent = "abalone"
    expected = "projects/{project}/agent/intents/{intent}".format(
        project=project,
        intent=intent,
    )
    actual = ParticipantsClient.intent_path(project, intent)
    assert expected == actual


def test_parse_intent_path():
    expected = {
        "project": "squid",
        "intent": "clam",
    }
    path = ParticipantsClient.intent_path(**expected)

    
    actual = ParticipantsClient.parse_intent_path(path)
    assert expected == actual


def test_message_path():
    project = "whelk"
    conversation = "octopus"
    message = "oyster"
    expected = (
        "projects/{project}/conversations/{conversation}/messages/{message}".format(
            project=project,
            conversation=conversation,
            message=message,
        )
    )
    actual = ParticipantsClient.message_path(project, conversation, message)
    assert expected == actual


def test_parse_message_path():
    expected = {
        "project": "nudibranch",
        "conversation": "cuttlefish",
        "message": "mussel",
    }
    path = ParticipantsClient.message_path(**expected)

    
    actual = ParticipantsClient.parse_message_path(path)
    assert expected == actual


def test_participant_path():
    project = "winkle"
    conversation = "nautilus"
    participant = "scallop"
    expected = "projects/{project}/conversations/{conversation}/participants/{participant}".format(
        project=project,
        conversation=conversation,
        participant=participant,
    )
    actual = ParticipantsClient.participant_path(project, conversation, participant)
    assert expected == actual


def test_parse_participant_path():
    expected = {
        "project": "abalone",
        "conversation": "squid",
        "participant": "clam",
    }
    path = ParticipantsClient.participant_path(**expected)

    
    actual = ParticipantsClient.parse_participant_path(path)
    assert expected == actual


def test_session_entity_type_path():
    project = "whelk"
    session = "octopus"
    entity_type = "oyster"
    expected = (
        "projects/{project}/agent/sessions/{session}/entityTypes/{entity_type}".format(
            project=project,
            session=session,
            entity_type=entity_type,
        )
    )
    actual = ParticipantsClient.session_entity_type_path(project, session, entity_type)
    assert expected == actual


def test_parse_session_entity_type_path():
    expected = {
        "project": "nudibranch",
        "session": "cuttlefish",
        "entity_type": "mussel",
    }
    path = ParticipantsClient.session_entity_type_path(**expected)

    
    actual = ParticipantsClient.parse_session_entity_type_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ParticipantsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = ParticipantsClient.common_billing_account_path(**expected)

    
    actual = ParticipantsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = ParticipantsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = ParticipantsClient.common_folder_path(**expected)

    
    actual = ParticipantsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = ParticipantsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = ParticipantsClient.common_organization_path(**expected)

    
    actual = ParticipantsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = ParticipantsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = ParticipantsClient.common_project_path(**expected)

    
    actual = ParticipantsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = ParticipantsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = ParticipantsClient.common_location_path(**expected)

    
    actual = ParticipantsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ParticipantsTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ParticipantsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ParticipantsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ParticipantsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_cancel_operation(transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = operations_pb2.CancelOperationRequest()

    
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        
        call.return_value = None
        response = client.cancel_operation(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc"):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = operations_pb2.CancelOperationRequest()

    
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    assert response is None


def test_cancel_operation_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None

        client.cancel_operation(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_cancel_operation_from_dict():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = operations_pb2.GetOperationRequest()

    
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc"):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = operations_pb2.GetOperationRequest()

    
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = operations_pb2.ListOperationsRequest()

    
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc"):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = operations_pb2.ListOperationsRequest()

    
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_locations(transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = locations_pb2.ListLocationsRequest()

    
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        
        call.return_value = locations_pb2.ListLocationsResponse()
        response = client.list_locations(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    assert isinstance(response, locations_pb2.ListLocationsResponse)


@pytest.mark.asyncio
async def test_list_locations_async(transport: str = "grpc"):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = locations_pb2.ListLocationsRequest()

    
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    assert isinstance(response, locations_pb2.ListLocationsResponse)


def test_list_locations_field_headers():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = locations_pb2.ListLocationsResponse()

        client.list_locations(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_locations_field_headers_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    
    
    request = locations_pb2.ListLocationsRequest()
    request.name = "locations"

    
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        await client.list_locations(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_locations_from_dict():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        
        call.return_value = locations_pb2.ListLocationsResponse()

        response = client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_locations_from_dict_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.ListLocationsResponse()
        )
        response = await client.list_locations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_location(transport: str = "grpc"):
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = locations_pb2.GetLocationRequest()

    
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        
        call.return_value = locations_pb2.Location()
        response = client.get_location(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    assert isinstance(response, locations_pb2.Location)


@pytest.mark.asyncio
async def test_get_location_async(transport: str = "grpc_asyncio"):
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    
    
    request = locations_pb2.GetLocationRequest()

    
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    assert isinstance(response, locations_pb2.Location)


def test_get_location_field_headers():
    client = ParticipantsClient(credentials=ga_credentials.AnonymousCredentials())

    
    
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = locations_pb2.Location()

        client.get_location(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_location_field_headers_async():
    client = ParticipantsAsyncClient(credentials=ga_credentials.AnonymousCredentials())

    
    
    request = locations_pb2.GetLocationRequest()
    request.name = "locations/abc"

    
    with mock.patch.object(type(client.transport.get_location), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        await client.get_location(request)
        
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations/abc",
    ) in kw["metadata"]


def test_get_location_from_dict():
    client = ParticipantsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        
        call.return_value = locations_pb2.Location()

        response = client.get_location(
            request={
                "name": "locations/abc",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_location_from_dict_async():
    client = ParticipantsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    
    with mock.patch.object(type(client.transport.list_locations), "__call__") as call:
        
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            locations_pb2.Location()
        )
        response = await client.get_location(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = ParticipantsClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = ParticipantsClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (ParticipantsClient, transports.ParticipantsGrpcTransport),
        (ParticipantsAsyncClient, transports.ParticipantsGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.p