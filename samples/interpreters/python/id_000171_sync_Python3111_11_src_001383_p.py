import asyncio
import re
from unittest import mock

from kafka.protocol.group import (
    JoinGroupRequest_v0 as JoinGroupRequest,
    SyncGroupResponse_v0 as SyncGroupResponse,
    LeaveGroupRequest_v0 as LeaveGroupRequest,
    HeartbeatRequest_v0 as HeartbeatRequest,
)
from kafka.protocol.commit import (
    OffsetCommitRequest, OffsetCommitResponse_v2,
    OffsetFetchRequest_v1 as OffsetFetchRequest
)
import kafka.errors as Errors

from ._testutil import KafkaIntegrationTestCase, run_until_complete

from aiokafka import ConsumerRebalanceListener
from aiokafka.client import AIOKafkaClient
from aiokafka.structs import OffsetAndMetadata, TopicPartition
from aiokafka.consumer.group_coordinator import (
    GroupCoordinator, CoordinatorGroupRebalance, NoGroupCoordinator)
from aiokafka.consumer.subscription_state import SubscriptionState
from aiokafka.util import create_future, create_task, get_running_loop

UNKNOWN_MEMBER_ID = JoinGroupRequest.UNKNOWN_MEMBER_ID


class RebalanceListenerForTest(ConsumerRebalanceListener):
    def __init__(self):
        self.revoked = []
        self.assigned = []

    def on_partitions_revoked(self, revoked):
        self.revoked.append(revoked)
        raise Exception("coordinator should ignore this exception")

    def on_partitions_assigned(self, assigned):
        self.assigned.append(assigned)
        raise Exception("coordinator should ignore this exception")


class TestKafkaCoordinatorIntegration(KafkaIntegrationTestCase):
    @run_until_complete
    async def test_coordinator_workflow(self):
        

        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        await self.wait_topic(client, 'topic1')
        await self.wait_topic(client, 'topic2')

        
        
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1', 'topic2'})
        coordinator = GroupCoordinator(
            client, subscription,
            session_timeout_ms=10000,
            heartbeat_interval_ms=500,
            retry_backoff_ms=100)

        self.assertEqual(coordinator.coordinator_id, None)
        self.assertTrue(coordinator.need_rejoin(subscription.subscription))

        await coordinator.ensure_coordinator_known()
        self.assertNotEqual(coordinator.coordinator_id, None)

        if subscription.subscription.assignment is None:
            await subscription.wait_for_assignment()
        self.assertNotEqual(coordinator.coordinator_id, None)
        self.assertFalse(coordinator.need_rejoin(subscription.subscription))

        tp_list = subscription.assigned_partitions()
        self.assertEqual(
            tp_list,
            {
                ('topic1', 0),
                ('topic1', 1),
                ('topic2', 0),
                ('topic2', 1)
            }
        )

        
        client2 = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client2.bootstrap()
        subscription2 = SubscriptionState()
        subscription2.subscribe(topics={'topic1', 'topic2'})
        coordinator2 = GroupCoordinator(
            client2, subscription2,
            session_timeout_ms=10000,
            heartbeat_interval_ms=500,
            retry_backoff_ms=100)
        await asyncio.gather(
            subscription.wait_for_assignment(),
            subscription2.wait_for_assignment()
        )

        tp_list = subscription.assigned_partitions()
        self.assertEqual(len(tp_list), 2)
        tp_list2 = subscription2.assigned_partitions()
        self.assertEqual(len(tp_list2), 2)
        tp_list |= tp_list2
        self.assertEqual(
            tp_list,
            {
                ('topic1', 0),
                ('topic1', 1),
                ('topic2', 0),
                ('topic2', 1)
            }
        )
        
        await coordinator.close()
        await client.close()

        await subscription2.wait_for_assignment()
        tp_list = subscription2.assigned_partitions()
        self.assertEqual(
            tp_list,
            {
                ('topic1', 0),
                ('topic1', 1),
                ('topic2', 0),
                ('topic2', 1)
            }
        )
        await coordinator2.close()
        await client2.close()

    @run_until_complete
    async def test_failed_group_join(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        await self.wait_topic(client, 'topic1')
        self.add_cleanup(client.close)

        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            retry_backoff_ms=10)
        coordinator._coordination_task.cancel()  
        try:
            await coordinator._coordination_task
        except asyncio.CancelledError:
            pass
        coordinator._coordination_task = create_task(
            asyncio.sleep(0.1)
        )
        coordinator.coordinator_id = 15
        self.add_cleanup(coordinator.close)

        async def _on_join_leader(resp):
            return b"123"

        _on_join_leader_mock = mock.Mock()
        _on_join_leader_mock.side_effect = _on_join_leader

        async def do_rebalance():
            rebalance = CoordinatorGroupRebalance(
                coordinator, coordinator.group_id, coordinator.coordinator_id,
                subscription.subscription, coordinator._assignors,
                coordinator._session_timeout_ms,
                coordinator._retry_backoff_ms)
            rebalance._on_join_leader = _on_join_leader_mock
            return (await rebalance.perform_group_join())

        mocked = mock.MagicMock()
        coordinator._client = mocked
        coordinator._client.api_version = (0, 10, 1)
        error_type = Errors.NoError

        async def send(*agrs, **kw):
            resp = JoinGroupRequest.RESPONSE_TYPE(
                error_code=error_type.errno,
                generation_id=-1,  
                group_protocol="roundrobin",
                leader_id="111",  
                member_id="111",  
                members=[]
            )
            return resp

        mocked.send.side_effect = send
        subsc = subscription.subscription

        
        resp = await do_rebalance()
        self.assertEqual(resp, ("roundrobin", b"123"))
        self.assertEqual(_on_join_leader_mock.call_count, 1)

        
        error_type = Errors.GroupLoadInProgressError
        resp = await do_rebalance()
        self.assertIsNone(resp)
        self.assertEqual(coordinator.need_rejoin(subsc), True)

        error_type = Errors.InvalidGroupIdError
        with self.assertRaises(Errors.InvalidGroupIdError):
            await do_rebalance()
        self.assertEqual(coordinator.need_rejoin(subsc), True)

        
        coordinator.member_id = 'some_invalid_member_id'
        error_type = Errors.UnknownMemberIdError
        resp = await do_rebalance()
        self.assertIsNone(resp)
        self.assertEqual(coordinator.need_rejoin(subsc), True)
        self.assertEqual(
            coordinator.member_id, JoinGroupRequest.UNKNOWN_MEMBER_ID)

        error_type = Errors.UnknownError()
        with self.assertRaises(Errors.KafkaError):  
            await do_rebalance()

        
        error_type = Errors.GroupCoordinatorNotAvailableError
        resp = await do_rebalance()
        self.assertIsNone(resp)
        self.assertEqual(coordinator.need_rejoin(subsc), True)
        self.assertEqual(coordinator.coordinator_id, None)
        coordinator.coordinator_id = 15
        coordinator._coordinator_dead_fut = create_future()

        async def _on_join_leader(resp):
            return None

        
        error_type = Errors.NoError
        _on_join_leader_mock.side_effect = _on_join_leader
        resp = await do_rebalance()
        self.assertEqual(coordinator.coordinator_id, 15)
        self.assertIsNone(resp)
        self.assertEqual(_on_join_leader_mock.call_count, 2)

        
        async def send_change_sub(*args, **kw):
            subscription.subscribe(topics={'topic2'})
            return (await send(*args, **kw))
        mocked.send.side_effect = send_change_sub
        resp = await do_rebalance()
        self.assertEqual(resp, None)
        self.assertEqual(_on_join_leader_mock.call_count, 2)

        
        mocked.send.side_effect = Errors.GroupCoordinatorNotAvailableError()
        resp = await do_rebalance()
        self.assertIsNone(resp)
        self.assertEqual(coordinator.need_rejoin(subsc), True)
        self.assertEqual(coordinator.coordinator_id, None)

    @run_until_complete
    async def test_failed_sync_group(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            heartbeat_interval_ms=20000)
        coordinator._coordination_task.cancel()  
        try:
            await coordinator._coordination_task
        except asyncio.CancelledError:
            pass
        coordinator._coordination_task = create_task(
            asyncio.sleep(0.1)
        )
        coordinator.coordinator_id = 15
        self.add_cleanup(coordinator.close)

        async def do_sync_group():
            rebalance = CoordinatorGroupRebalance(
                coordinator, coordinator.group_id, coordinator.coordinator_id,
                subscription.subscription, coordinator._assignors,
                coordinator._session_timeout_ms,
                coordinator._retry_backoff_ms)
            await rebalance._on_join_follower()

        mocked = mock.MagicMock()
        coordinator._client = mocked
        coordinator._client.api_version = (0, 10, 1)
        subsc = subscription.subscription
        error_type = None

        async def send(*agrs, **kw):
            resp = SyncGroupResponse(
                error_code=error_type.errno,
                member_assignment=b"123"
            )
            return resp

        mocked.send.side_effect = send

        coordinator.member_id = 'some_invalid_member_id'

        error_type = Errors.RebalanceInProgressError
        await do_sync_group()
        self.assertEqual(coordinator.member_id, 'some_invalid_member_id')
        self.assertEqual(coordinator.need_rejoin(subsc), True)

        error_type = Errors.UnknownMemberIdError
        await do_sync_group()
        self.assertEqual(coordinator.member_id, UNKNOWN_MEMBER_ID)
        self.assertEqual(coordinator.need_rejoin(subsc), True)

        error_type = Errors.NotCoordinatorForGroupError
        await do_sync_group()
        self.assertEqual(coordinator.coordinator_id, None)
        self.assertEqual(coordinator.need_rejoin(subsc), True)
        coordinator.coordinator_id = 15
        coordinator._coordinator_dead_fut = create_future()

        error_type = Errors.UnknownError()
        with self.assertRaises(Errors.KafkaError):  
            await do_sync_group()
        self.assertEqual(coordinator.need_rejoin(subsc), True)

        error_type = Errors.GroupAuthorizationFailedError()
        with self.assertRaises(Errors.GroupAuthorizationFailedError) as cm:
            await do_sync_group()
        self.assertEqual(coordinator.need_rejoin(subsc), True)
        self.assertEqual(cm.exception.args[0], coordinator.group_id)

        
        mocked.send.side_effect = Errors.GroupCoordinatorNotAvailableError()
        await do_sync_group()
        self.assertEqual(coordinator.coordinator_id, None)
        self.assertEqual(coordinator.need_rejoin(subsc), True)

    @run_until_complete
    async def test_generation_change_during_rejoin_sync(self):
        coordinator = mock.MagicMock()
        subscription = mock.MagicMock()
        assignors = mock.MagicMock()
        member_assignment = mock.Mock()

        rebalance = CoordinatorGroupRebalance(
            coordinator, "group_id", "coordinator_id", subscription,
            assignors, 1000, 1000)

        async def send_req(request):
            await asyncio.sleep(0.1)
            resp = mock.MagicMock()
            resp.member_assignment = member_assignment
            resp.error_code = 0
            return resp

        coordinator._send_req.side_effect = send_req

        request = mock.MagicMock()
        coordinator.generation = 1
        coordinator.member_id = "member_id"
        sync_req = asyncio.ensure_future(rebalance._send_sync_group_request(request))
        await asyncio.sleep(0.05)

        coordinator.generation = -1
        coordinator.member_id = "member_id-changed"

        assert await sync_req == member_assignment

        
        assert coordinator.generation == 1
        assert coordinator.member_id == "member_id"

    @run_until_complete
    async def test_subscribe_pattern(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()

        test_listener = RebalanceListenerForTest()
        subscription = SubscriptionState()
        coordinator = GroupCoordinator(
            client, subscription,
            group_id='subs-pattern-group')

        await self.wait_topic(client, 'st-topic1')
        await self.wait_topic(client, 'st-topic2')

        subscription.subscribe_pattern(
            re.compile('st-topic*'), listener=test_listener)
        client.set_topics([])
        await subscription.wait_for_assignment()

        self.assertNotEqual(coordinator.coordinator_id, None)
        self.assertFalse(coordinator.need_rejoin(subscription.subscription))

        tp_list = subscription.assigned_partitions()
        assigned = {
            ('st-topic1', 0),
            ('st-topic1', 1),
            ('st-topic2', 0),
            ('st-topic2', 1),
        }
        self.assertEqual(tp_list, assigned)

        self.assertEqual(test_listener.revoked, [set()])
        self.assertEqual(test_listener.assigned, [assigned])
        await coordinator.close()
        await client.close()

    @run_until_complete
    async def test_commit_failed_scenarios(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        await self.wait_topic(client, 'topic1')
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            group_id='test-offsets-group')

        await subscription.wait_for_assignment()
        assignment = subscription.subscription.assignment

        offsets = {TopicPartition('topic1', 0): OffsetAndMetadata(1, '')}
        await coordinator.commit_offsets(assignment, offsets)

        _orig_send_req = coordinator._send_req
        with mock.patch.object(coordinator, "_send_req") as mocked:
            commit_error = None

            async def mock_send_req(request):
                if request.API_KEY == OffsetCommitRequest[0].API_KEY:
                    if isinstance(commit_error, list):
                        error_code = commit_error.pop(0).errno
                    else:
                        error_code = commit_error.errno
                    resp_topics = [("topic1", [(0, error_code)])]
                    return OffsetCommitResponse_v2(resp_topics)
                return (await _orig_send_req(request))
            mocked.side_effect = mock_send_req

            
            commit_error = Errors.GroupAuthorizationFailedError
            with self.assertRaises(Errors.GroupAuthorizationFailedError):
                await coordinator.commit_offsets(assignment, offsets)

            commit_error = Errors.TopicAuthorizationFailedError
            with self.assertRaises(Errors.TopicAuthorizationFailedError):
                await coordinator.commit_offsets(assignment, offsets)

            commit_error = Errors.InvalidCommitOffsetSizeError
            with self.assertRaises(Errors.InvalidCommitOffsetSizeError):
                await coordinator.commit_offsets(assignment, offsets)

            commit_error = Errors.OffsetMetadataTooLargeError
            with self.assertRaises(Errors.OffsetMetadataTooLargeError):
                await coordinator.commit_offsets(assignment, offsets)

            
            commit_error = [
                Errors.GroupLoadInProgressError,
                Errors.GroupLoadInProgressError,
                Errors.NoError,
            ]
            await coordinator.commit_offsets(assignment, offsets)

            
            commit_error = Errors.RebalanceInProgressError
            with self.assertRaises(Errors.CommitFailedError):
                await coordinator.commit_offsets(assignment, offsets)
            self.assertTrue(coordinator.need_rejoin(subscription.subscription))
            self.assertNotEqual(coordinator.member_id, UNKNOWN_MEMBER_ID)
            await subscription.wait_for_assignment()
            assignment = subscription.subscription.assignment

            commit_error = Errors.UnknownMemberIdError
            was_member_id = coordinator.member_id
            with self.assertRaises(Errors.CommitFailedError):
                await coordinator.commit_offsets(assignment, offsets)
            self.assertTrue(coordinator.need_rejoin(subscription.subscription))
            self.assertEqual(coordinator.member_id, UNKNOWN_MEMBER_ID)
            
            
            
            request = LeaveGroupRequest(coordinator.group_id, was_member_id)
            await coordinator._send_req(request)
            await subscription.wait_for_assignment()
            assignment = subscription.subscription.assignment

            
            commit_error = [
                Errors.GroupCoordinatorNotAvailableError,
                Errors.NoError
            ]
            await coordinator.commit_offsets(assignment, offsets)
            commit_error = [
                Errors.NotCoordinatorForGroupError,
                Errors.NoError
            ]
            await coordinator.commit_offsets(assignment, offsets)
            commit_error = [
                Errors.RequestTimedOutError,
                Errors.NoError
            ]
            await coordinator.commit_offsets(assignment, offsets)

            
            for retriable_error in (
                    Errors.GroupCoordinatorNotAvailableError,
                    Errors.NotCoordinatorForGroupError,
                    Errors.RequestTimedOutError,
            ):
                self.assertIsNotNone(coordinator.coordinator_id)
                commit_error = retriable_error
                with self.assertRaises(retriable_error):
                    await coordinator._do_commit_offsets(assignment, offsets)
                self.assertIsNone(coordinator.coordinator_id)

                
                await coordinator.ensure_coordinator_known()

            
            commit_error = Errors.UnknownError
            with self.assertRaises(Errors.UnknownError):
                await coordinator.commit_offsets(assignment, offsets)

        await coordinator.close()
        await client.close()

    @run_until_complete
    async def test_fetchoffsets_failed_scenarios(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        await self.wait_topic(client, 'topic1')
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            group_id='fetch-offsets-group')
        await subscription.wait_for_assignment()

        tp = TopicPartition('topic1', 0)
        partitions = {tp}
        _orig_send_req = coordinator._send_req
        with mock.patch.object(coordinator, "_send_req") as mocked:
            fetch_error = None

            async def mock_send_req(request):
                if request.API_KEY == OffsetFetchRequest.API_KEY:
                    if isinstance(fetch_error, list):
                        error_code = fetch_error.pop(0).errno
                    else:
                        error_code = fetch_error.errno
                    if error_code == Errors.NoError.errno:
                        offset = 10
                    else:
                        offset = -1
                    resp_topics = [("topic1", [(0, offset, "", error_code)])]
                    return request.RESPONSE_TYPE(resp_topics)
                return (await _orig_send_req(request))
            mocked.side_effect = mock_send_req

            
            res = await coordinator.fetch_committed_offsets({})
            self.assertEqual(res, {})
            self.assertEqual(mocked.call_count, 0)

            fetch_error = [
                Errors.GroupLoadInProgressError,
                Errors.GroupLoadInProgressError,
                Errors.NoError,
                Errors.NoError,
                Errors.NoError
            ]
            res = await coordinator.fetch_committed_offsets(partitions)
            self.assertEqual(res, {tp: OffsetAndMetadata(10, "")})

            
            fetch_error = Errors.UnknownTopicOrPartitionError
            res = await coordinator.fetch_committed_offsets(partitions)
            self.assertEqual(res, {})

            fetch_error = [
                Errors.NotCoordinatorForGroupError,
                Errors.NotCoordinatorForGroupError,
                Errors.NoError,
                Errors.NoError,
                Errors.NoError
            ]
            r = await coordinator.fetch_committed_offsets(partitions)
            self.assertEqual(r, {tp: OffsetAndMetadata(10, "")})

            fetch_error = Errors.GroupAuthorizationFailedError
            with self.assertRaises(Errors.GroupAuthorizationFailedError) as cm:
                await coordinator.fetch_committed_offsets(partitions)
            self.assertEqual(cm.exception.args[0], coordinator.group_id)

            fetch_error = Errors.UnknownError
            with self.assertRaises(Errors.KafkaError):
                await coordinator.fetch_committed_offsets(partitions)

        await coordinator.close()
        await client.close()

    @run_until_complete
    async def test_coordinator_subscription_replace_on_rebalance(self):
        
        client = AIOKafkaClient(
            metadata_max_age_ms=2000,
            bootstrap_servers=self.hosts)
        await client.bootstrap()
        await self.wait_topic(client, 'topic1')
        await self.wait_topic(client, 'topic2')
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        client.set_topics(('topic1', ))
        coordinator = GroupCoordinator(
            client, subscription,
            group_id='race-rebalance-subscribe-replace',
            heartbeat_interval_ms=1000)

        _perform_assignment = coordinator._perform_assignment
        with mock.patch.object(coordinator, '_perform_assignment') as mocked:

            async def _new(*args, **kw):
                
                
                res = await _perform_assignment(*args, **kw)
                if subscription.subscription.topics == {"topic1"}:
                    subscription.subscribe(topics={'topic2'})
                    client.set_topics(('topic2', ))
                return res
            mocked.side_effect = _new

            await subscription.wait_for_assignment()
            topics = {
                tp.topic for tp in subscription.assigned_partitions()}
            self.assertEqual(topics, {'topic2'})

            
            self.assertEqual(mocked.call_count, 2)

        await coordinator.close()
        await client.close()

    @run_until_complete
    async def test_coordinator_subscription_append_on_rebalance(self):
        
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        await self.wait_topic(client, 'topic1')
        await self.wait_topic(client, 'topic2')
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            group_id='race-rebalance-subscribe-append',
            heartbeat_interval_ms=20000000)

        _perform_assignment = coordinator._perform_assignment
        with mock.patch.object(coordinator, '_perform_assignment') as mocked:

            async def _new(*args, **kw):
                
                
                res = await _perform_assignment(*args, **kw)
                if subscription.subscription.topics == {"topic1"}:
                    subscription.subscribe(topics={'topic1', 'topic2'})
                    client.set_topics(('topic1', 'topic2', ))
                return res
            mocked.side_effect = _new

            await subscription.wait_for_assignment()
            topics = {
                tp.topic for tp in subscription.assigned_partitions()}
            self.assertEqual(topics, {'topic1', 'topic2'})

            
            self.assertEqual(mocked.call_count, 2)

        await coordinator.close()
        await client.close()

    @run_until_complete
    async def test_coordinator_metadata_update_during_rebalance(self):
        
        

        
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        await self.wait_topic(client, 'topic1')
        await self.wait_topic(client, 'topic2')
        await client.close()

        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        self.add_cleanup(client.close)
        subscription = SubscriptionState()
        client.set_topics(("topic1", ))
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            group_id='race-rebalance-metadata-update',
            heartbeat_interval_ms=20000000)
        self.add_cleanup(coordinator.close)
        await subscription.wait_for_assignment()
        
        self.assertEqual(
            subscription.assigned_partitions(),
            {TopicPartition("topic1", 0), TopicPartition("topic1", 1)})

        _metadata_update = client._metadata_update
        with mock.patch.object(client, '_metadata_update') as mocked:
            async def _new(*args, **kw):
                
                
                await asyncio.sleep(0.5)
                res = await _metadata_update(*args, **kw)
                return res
            mocked.side_effect = _new

            
            
            
            subscription.subscribe(topics={'topic2'})
            client.set_topics(('topic2', ))
            await subscription.wait_for_assignment()
            self.assertEqual(
                subscription.assigned_partitions(),
                {TopicPartition("topic2", 0), TopicPartition("topic2", 1)})

    @run_until_complete
    async def test_coordinator_metadata_change_by_broker(self):
        
        
        client = AIOKafkaClient(
            bootstrap_servers=self.hosts)
        await client.bootstrap()
        await self.wait_topic(client, 'topic1')
        await self.wait_topic(client, 'topic2')
        client.set_topics(['other_topic'])
        await client.force_metadata_update()

        subscription = SubscriptionState()
        coordinator = GroupCoordinator(
            client, subscription,
            group_id='race-rebalance-subscribe-append',
            heartbeat_interval_ms=2000000)
        subscription.subscribe(topics={'topic1'})
        await client.set_topics(('topic1', ))
        await subscription.wait_for_assignment()

        _perform_assignment = coordinator._perform_assignment
        with mock.patch.object(coordinator, '_perform_assignment') as mocked:
            mocked.side_effect = _perform_assignment

            subscription.subscribe(topics={'topic2'})
            await client.set_topics(('topic2', ))

            
            
            
            
            
            await subscription.wait_for_assignment()
            await client.force_metadata_update()
            self.assertFalse(
                coordinator.need_rejoin(subscription.subscription))
            self.assertEqual(mocked.call_count, 1)

        await coordinator.close()
        await client.close()

    @run_until_complete
    async def test_coordinator_ensure_active_group_on_expired_membership(self):
        
        
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        await self.wait_topic(client, 'topic1')
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            group_id='test-offsets-group', session_timeout_ms=6000,
            heartbeat_interval_ms=1000)
        await subscription.wait_for_assignment()
        assignment = subscription.subscription.assignment

        
        tp = TopicPartition('topic1', 0)
        subscription.seek(tp, 0)
        offsets = assignment.all_consumed_offsets()
        self.assertTrue(offsets)  

        
        _orig_send_req = coordinator._send_req
        resp_topics = [("topic1", [(0, Errors.UnknownMemberIdError.errno)])]
        with mock.patch.object(coordinator, "_send_req") as mocked:
            async def mock_send_req(request):
                if request.API_KEY == OffsetCommitRequest[0].API_KEY:
                    return OffsetCommitResponse_v2(resp_topics)
                return (await _orig_send_req(request))
            mocked.side_effect = mock_send_req

            with self.assertRaises(Errors.CommitFailedError):
                await coordinator.commit_offsets(assignment, offsets)
            self.assertTrue(coordinator.need_rejoin(subscription.subscription))
            
            await subscription.wait_for_assignment()

        await coordinator.close()
        await client.close()

    @run_until_complete
    async def test_coordinator__send_req(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        self.add_cleanup(client.close)
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            group_id='test-my-group', session_timeout_ms=6000,
            heartbeat_interval_ms=1000)
        self.add_cleanup(coordinator.close)

        request = OffsetCommitRequest[2](topics=[])

        
        with self.assertRaises(Errors.GroupCoordinatorNotAvailableError):
            await coordinator._send_req(request)

        await coordinator.ensure_coordinator_known()
        self.assertIsNotNone(coordinator.coordinator_id)

        with mock.patch.object(client, "send") as mocked:
            async def mock_send(*args, **kw):
                raise Errors.KafkaError("Some unexpected error")
            mocked.side_effect = mock_send

            
            with self.assertRaises(Errors.KafkaError):
                await coordinator._send_req(request)
            self.assertIsNone(coordinator.coordinator_id)

    @run_until_complete
    async def test_coordinator_close(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        self.add_cleanup(client.close)
        subscription = SubscriptionState()
        waiter = create_future()

        class WaitingListener(ConsumerRebalanceListener):
            def on_partitions_revoked(self, revoked):
                pass

            async def on_partitions_assigned(self, assigned, waiter=waiter):
                await waiter

        coordinator = GroupCoordinator(
            client, subscription,
            group_id='test-my-group', session_timeout_ms=6000,
            heartbeat_interval_ms=1000)
        subscription.subscribe(
            topics={'topic1'}, listener=WaitingListener())

        
        close_task = create_task(coordinator.close())
        await asyncio.sleep(0.1)
        self.assertFalse(close_task.done())

        
        waiter.set_result(True)
        await close_task

        
        await coordinator.close()

    @run_until_complete
    async def test_coordinator_close_autocommit(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        self.add_cleanup(client.close)
        subscription = SubscriptionState()
        coordinator = GroupCoordinator(
            client, subscription,
            group_id='test-my-group', session_timeout_ms=6000,
            heartbeat_interval_ms=1000)
        subscription.subscribe(topics={'topic1'})
        await subscription.wait_for_assignment()

        waiter = create_future()

        async def commit_offsets(*args, **kw):
            await waiter

        coordinator.commit_offsets = mocked = mock.Mock()
        mocked.side_effect = commit_offsets

        
        close_task = create_task(coordinator.close())
        await asyncio.sleep(0.1)
        

        
        
        waiter.set_exception(Errors.UnknownError())
        await close_task

    @run_until_complete
    async def test_coordinator_ensure_coordinator_known(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            heartbeat_interval_ms=20000)
        coordinator._coordination_task.cancel()  
        try:
            await coordinator._coordination_task
        except asyncio.CancelledError:
            pass
        coordinator._coordination_task = create_task(
            asyncio.sleep(0.1,)
        )
        self.add_cleanup(coordinator.close)

        def force_metadata_update():
            fut = create_future()
            fut.set_result(True)
            return fut

        client.ready = mock.Mock()
        client.force_metadata_update = mock.Mock()
        client.force_metadata_update.side_effect = force_metadata_update

        async def ready(node_id, group=None):
            if node_id == 0:
                return True
            return False
        client.ready.side_effect = ready
        client.coordinator_lookup = mock.Mock()

        coordinator_lookup = None

        async def _do_coordinator_lookup(type_, key):
            node_id = coordinator_lookup.pop()
            if isinstance(node_id, Exception):
                raise node_id
            return node_id
        client.coordinator_lookup.side_effect = _do_coordinator_lookup

        
        
        
        coordinator.coordinator_dead()
        coordinator_lookup = [0, 1, 1]
        await coordinator.ensure_coordinator_known()
        self.assertEqual(coordinator.coordinator_id, 0)
        self.assertEqual(client.force_metadata_update.call_count, 0)

        
        
        coordinator.coordinator_dead()
        coordinator_lookup = [0, Errors.UnknownTopicOrPartitionError()]
        await coordinator.ensure_coordinator_known()
        self.assertEqual(client.force_metadata_update.call_count, 1)

        
        coordinator.coordinator_dead()
        coordinator_lookup = [0, Errors.GroupAuthorizationFailedError()]
        with self.assertRaises(Errors.GroupAuthorizationFailedError) as cm:
            await coordinator.ensure_coordinator_known()
        self.assertEqual(cm.exception.args[0], coordinator.group_id)

        
        coordinator.coordinator_dead()
        coordinator_lookup = [0, Errors.UnknownError()]
        with self.assertRaises(Errors.UnknownError):
            await coordinator.ensure_coordinator_known()

    @run_until_complete
    async def test_coordinator__do_heartbeat(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            heartbeat_interval_ms=20000)
        coordinator._coordination_task.cancel()  
        try:
            await coordinator._coordination_task
        except asyncio.CancelledError:
            pass
        coordinator._coordination_task = create_task(
            asyncio.sleep(0.1)
        )
        self.add_cleanup(coordinator.close)

        _orig_send_req = coordinator._send_req
        coordinator._send_req = mocked = mock.Mock()
        heartbeat_error = None
        send_req_error = None

        async def mock_send_req(request):
            if send_req_error is not None:
                raise send_req_error
            if request.API_KEY == HeartbeatRequest.API_KEY:
                if isinstance(heartbeat_error, list):
                    error_code = heartbeat_error.pop(0).errno
                else:
                    error_code = heartbeat_error.errno
                return HeartbeatRequest.RESPONSE_TYPE(error_code)
            return (await _orig_send_req(request))
        mocked.side_effect = mock_send_req

        coordinator.coordinator_id = 15
        heartbeat_error = Errors.GroupCoordinatorNotAvailableError()
        success = await coordinator._do_heartbeat()
        self.assertFalse(success)
        self.assertIsNone(coordinator.coordinator_id)

        coordinator._rejoin_needed_fut = create_future()
        heartbeat_error = Errors.RebalanceInProgressError()
        success = await coordinator._do_heartbeat()
        self.assertTrue(success)
        self.assertTrue(coordinator._rejoin_needed_fut.done())

        coordinator.member_id = "some_member"
        coordinator._rejoin_needed_fut = create_future()
        heartbeat_error = Errors.IllegalGenerationError()
        success = await coordinator._do_heartbeat()
        self.assertFalse(success)
        self.assertTrue(coordinator._rejoin_needed_fut.done())
        self.assertEqual(coordinator.member_id, UNKNOWN_MEMBER_ID)

        coordinator.member_id = "some_member"
        coordinator._rejoin_needed_fut = create_future()
        heartbeat_error = Errors.UnknownMemberIdError()
        success = await coordinator._do_heartbeat()
        self.assertFalse(success)
        self.assertTrue(coordinator._rejoin_needed_fut.done())
        self.assertEqual(coordinator.member_id, UNKNOWN_MEMBER_ID)

        heartbeat_error = Errors.GroupAuthorizationFailedError()
        with self.assertRaises(Errors.GroupAuthorizationFailedError) as cm:
            await coordinator._do_heartbeat()
        self.assertEqual(cm.exception.args[0], coordinator.group_id)

        heartbeat_error = Errors.UnknownError()
        with self.assertRaises(Errors.KafkaError):
            await coordinator._do_heartbeat()

        heartbeat_error = None
        send_req_error = Errors.RequestTimedOutError()
        success = await coordinator._do_heartbeat()
        self.assertFalse(success)

        heartbeat_error = Errors.NoError()
        send_req_error = None
        success = await coordinator._do_heartbeat()
        self.assertTrue(success)

    @run_until_complete
    async def test_coordinator__heartbeat_routine(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        subscription = SubscriptionState()
        subscription.subscribe(topics={'topic1'})
        coordinator = GroupCoordinator(
            client, subscription,
            heartbeat_interval_ms=100,
            session_timeout_ms=300,
            retry_backoff_ms=50)
        coordinator._coordination_task.cancel()  
        try:
            await coordinator._coordination_task
        except asyncio.CancelledError:
            pass
        coordinator._coordination_task = create_task(
            asyncio.sleep(0.1)
        )
        self.add_cleanup(coordinator.close)

        coordinator._do_heartbeat = mocked = mock.Mock()
        coordinator.coordinator_id = 15
        coordinator.member_id = 17
        coordinator.generation = 0
        success = None

        async def _do_heartbeat(*args, **kw):
            if isinstance(success, list):
                return success.pop(0)
            return success
        mocked.side_effect = _do_heartbeat

        async def ensure_coordinator_known():
            return None

        coordinator.ensure_coordinator_known = mock.Mock()
        coordinator.ensure_coordinator_known.side_effect = (
            ensure_coordinator_known
        )

        routine = create_task(
            coordinator._heartbeat_routine())

        def cleanup():
            routine.cancel()
            return routine
        self.add_cleanup(cleanup)

        
        success = True
        await asyncio.sleep(0.13)
        self.assertFalse(routine.done())
        self.assertEqual(mocked.call_count, 1)

        
        success = False
        await asyncio.sleep(0.15)
        self.assertFalse(routine.done())
        
        self.assertEqual(mocked.call_count, 3)

        
        await asyncio.sleep(0.10)
        self.assertEqual(mocked.call_count, 5)
        self.assertEqual(coordinator.coordinator_id, 15)
        
        await asyncio.sleep(0.05)
        self.assertEqual(mocked.call_count, 6)
        self.assertIsNone(coordinator.coordinator_id)

    @run_until_complete
    async def test_coordinator__maybe_refresh_commit_offsets(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        subscription = SubscriptionState()
        tp = TopicPartition("topic1", 0)
        coordinator = GroupCoordinator(
            client, subscription,
            heartbeat_interval_ms=20000)
        coordinator._coordination_task.cancel()  
        try:
            await coordinator._coordination_task
        except asyncio.CancelledError:
            pass
        coordinator._coordination_task = create_task(
            asyncio.sleep(0.1)
        )
        self.add_cleanup(coordinator.close)

        coordinator._do_fetch_commit_offsets = mocked = mock.Mock()
        fetched_offsets = {tp: OffsetAndMetadata(12, "")}
        test_self = self

        async def do_fetch(need_update):
            test_self.assertEqual(need_update, [tp])
            return fetched_offsets
        mocked.side_effect = do_fetch

        def reset_assignment():
            subscription.assign_from_user({tp})
            assignment = subscription.subscription.assignment
            tp_state = assignment.state_value(tp)
            fut = tp_state.fetch_committed()
            return assignment, tp_state, fut
        assignment, tp_state, fut = reset_assignment()

        
        resp = await coordinator._maybe_refresh_commit_offsets(assignment)
        self.assertEqual(resp, True)
        self.assertEqual(fut.result(), OffsetAndMetadata(12, ""))

        
        resp = await coordinator._maybe_refresh_commit_offsets(assignment)
        self.assertEqual(resp, True)
        self.assertEqual(mocked.call_count, 1)

        
        fetched_offsets = {}
        assignment, tp_state, fut = reset_assignment()
        resp = await coordinator._maybe_refresh_commit_offsets(assignment)
        self.assertEqual(resp, True)
        self.assertEqual(fut.result(), OffsetAndMetadata(-1, ""))

        
        assignment, tp_state, fut = reset_assignment()
        mocked.side_effect = Errors.GroupCoordinatorNotAvailableError()
        resp = await coordinator._maybe_refresh_commit_offsets(assignment)
        self.assertEqual(resp, False)

        
        mocked.side_effect = Errors.UnknownError()
        with self.assertRaises(Errors.UnknownError):
            await coordinator._maybe_refresh_commit_offsets(assignment)

    @run_until_complete
    async def test_coordinator__maybe_do_autocommit(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        subscription = SubscriptionState()
        tp = TopicPartition("topic1", 0)
        coordinator = GroupCoordinator(
            client, subscription,
            heartbeat_interval_ms=20000, auto_commit_interval_ms=1000,
            retry_backoff_ms=50)
        coordinator._coordination_task.cancel()  
        try:
            await coordinator._coordination_task
        except asyncio.CancelledError:
            pass
        coordinator._coordination_task = create_task(
            asyncio.sleep(0.1)
        )
        self.add_cleanup(coordinator.close)

        coordinator._do_commit_offsets = mocked = mock.Mock()

        async def do_commit(*args, **kw):
            await asyncio.sleep(0.1)
            return
        mocked.side_effect = do_commit

        def reset_assignment():
            subscription.assign_from_user({tp})
            assignment = subscription.subscription.assignment
            tp_state = assignment.state_value(tp)
            return assignment, tp_state
        assignment, tp_state = reset_assignment()

        
        coordinator._enable_auto_commit = False
        timeout = await coordinator._maybe_do_autocommit(assignment)
        self.assertIsNone(timeout)  
        self.assertEqual(mocked.call_count, 0)
        coordinator._enable_auto_commit = True

        
        loop = get_running_loop()
        now = loop.time()
        interval = 1
        coordinator._next_autocommit_deadline = 0
        timeout = await coordinator._maybe_do_autocommit(assignment)
        
        self.assertAlmostEqual(timeout, 0.9, places=1)
        self.assertAlmostEqual(
            coordinator._next_autocommit_deadline, now + interval, places=1)
        self.assertEqual(mocked.call_count, 1)

        
        coordinator._next_autocommit_deadline = 0
        mocked.side_effect = Errors.NotCoordinatorForGroupError()
        now = loop.time()
        timeout = await coordinator._maybe_do_autocommit(assignment)
        self.assertEqual(timeout, 0.05)
        
        
        self.assertAlmostEqual(
            coordinator._next_autocommit_deadline, now + timeout,
            places=1)

        
        coordinator._next_autocommit_deadline = 0
        mocked.side_effect = Errors.UnknownMemberIdError()
        now = loop.time()
        timeout = await coordinator._maybe_do_autocommit(assignment)
        self.assertEqual(timeout, 0.05)

        
        mocked.side_effect = Errors.UnknownError()
        now = loop.time()
        coordinator._next_autocommit_deadline = 0
        with self.assertRaises(Errors.KafkaError):
            await coordinator._maybe_do_autocommit(assignment)

    @run_until_complete
    async def test_coordinator__coordination_routine(self):
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        subscription = SubscriptionState()
        tp = TopicPartition("topic1", 0)
        coordinator = GroupCoordinator(
            client, subscription,
            heartbeat_interval_ms=20000, auto_commit_interval_ms=1000,
            retry_backoff_ms=50)
        self.add_cleanup(coordinator.close)

        def start_coordination():
            if coordinator._coordination_task:
                coordinator._coordination_task.cancel()
            coordinator._coordination_task = task = create_task(
                coordinator._coordination_routine())
            return task

        async def stop_coordination():
            coordinator._coordination_task.cancel()  
            try:
                await coordinator._coordination_task
            except asyncio.CancelledError:
                pass
            coordinator._coordination_task = create_task(
                asyncio.sleep(0.1))

        await stop_coordination()

        async def ensure_coordinator_known():
            return None

        coordinator.ensure_coordinator_known = coord_mock = mock.Mock()
        coord_mock.side_effect = ensure_coordinator_known

        async def _on_join_prepare(assign):
            return None

        coordinator._on_join_prepare = prepare_mock = mock.Mock()
        prepare_mock.side_effect = _on_join_prepare

        coordinator._do_rejoin_group = rejoin_mock = mock.Mock()
        rejoin_ok = True

        async def do_rejoin(subsc):
            if rejoin_ok:
                subscription.assign_from_subscribed({tp})
                coordinator._rejoin_needed_fut = create_future()
                return True
            else:
                await asyncio.sleep(0.1)
                return False
        rejoin_mock.side_effect = do_rejoin

        async def _maybe_do_autocommit(assign):
            return None

        coordinator._maybe_do_autocommit = autocommit_mock = mock.Mock()
        autocommit_mock.side_effect = _maybe_do_autocommit
        coordinator._start_heartbeat_task = mock.Mock()

        client.force_metadata_update = metadata_mock = mock.Mock()
        done_fut = create_future()
        done_fut.set_result(None)
        metadata_mock.side_effect = lambda: done_fut

        
        
        task = start_coordination()
        await asyncio.sleep(0.01)
        self.assertFalse(task.done())
        self.assertEqual(coord_mock.call_count, 0)

        
        subscription.assign_from_user({tp})
        await asyncio.sleep(0.01)
        self.assertFalse(task.done())
        self.assertEqual(coord_mock.call_count, 1)
        self.assertEqual(prepare_mock.call_count, 0)
        self.assertEqual(rejoin_mock.call_count, 0)
        self.assertEqual(autocommit_mock.call_count, 1)

        
        coordinator.request_rejoin()
        await asyncio.sleep(0.01)
        self.assertFalse(task.done())
        self.assertEqual(coord_mock.call_count, 1)
        self.assertEqual(prepare_mock.call_count, 0)
        self.assertEqual(rejoin_mock.call_count, 0)
        self.assertEqual(autocommit_mock.call_count, 1)
        coordinator._rejoin_needed_fut = create_future()

        
        subscription.unsubscribe()
        subscription.subscribe({"topic1"})
        await asyncio.sleep(0.01)
        self.assertFalse(task.done())
        self.assertEqual(coord_mock.call_count, 2)
        self.assertEqual(prepare_mock.call_count, 1)
        self.assertEqual(rejoin_mock.call_count, 1)
        self.assertEqual(autocommit_mock.call_count, 2)

        
        rejoin_ok = False
        coordinator.request_rejoin()
        await asyncio.sleep(0.01)
        self.assertFalse(task.done())
        self.assertEqual(coord_mock.call_count, 3)
        self.assertEqual(prepare_mock.call_count, 2)
        self.assertEqual(rejoin_mock.call_count, 2)
        self.assertEqual(autocommit_mock.call_count, 2)

        
        rejoin_ok = True
        await subscription.wait_for_assignment()
        self.assertFalse(task.done())
        self.assertEqual(coord_mock.call_count, 4)
        self.assertEqual(prepare_mock.call_count, 2)
        self.assertEqual(rejoin_mock.call_count, 3)
        self.assertEqual(autocommit_mock.call_count, 3)

        
        
        subscription.unsubscribe()
        subscription.subscribe_pattern(re.compile("^topic1&"))
        subscription.subscribe_from_pattern({"topic1"})
        self.assertEqual(metadata_mock.call_count, 0)
        await asyncio.sleep(0.01)
        self.assertFalse(task.done())
        self.assertEqual(coord_mock.call_count, 5)
        self.assertEqual(prepare_mock.call_count, 3)
        self.assertEqual(rejoin_mock.call_count, 4)
        self.assertEqual(autocommit_mock.call_count, 4)
        self.assertEqual(metadata_mock.call_count, 1)

        
        subscription.unsubscribe()
        await asyncio.sleep(0.01)
        self.assertFalse(task.done())
        self.assertEqual(coord_mock.call_count, 5)
        self.assertEqual(prepare_mock.call_count, 3)
        self.assertEqual(rejoin_mock.call_count, 4)
        self.assertEqual(autocommit_mock.call_count, 4)
        self.assertEqual(metadata_mock.call_count, 1)

        
        coordinator._maybe_do_last_autocommit = last_commit_mock = mock.Mock()
        last_commit_mock.side_effect = Errors.UnknownError()
        await coordinator.close()
        self.assertTrue(task.done())

        
        self.assertEqual(coord_mock.call_count, 5)
        self.assertEqual(prepare_mock.call_count, 3)
        self.assertEqual(rejoin_mock.call_count, 4)
        self.assertEqual(autocommit_mock.call_count, 4)
        self.assertEqual(metadata_mock.call_count, 1)
        self.assertEqual(last_commit_mock.call_count, 1)

    @run_until_complete
    async def test_no_group_subscribe_during_metadata_update(self):
        
        
        client = AIOKafkaClient(bootstrap_servers=self.hosts)
        await client.bootstrap()
        await self.wait_topic(client, 'topic1')
        await self.wait_topic(client, 'topic2')
        await client.set_topics(('other_topic', ))

        subscription = SubscriptionState()
        coordinator = NoGroupCoordinator(
            client, subscription)
        subscription.subscribe(topics={'topic1'})
        client.set_topics(('topic1', ))
        await asyncio.sleep(0.0001)

        
        subscription.subscribe(topics={'topic2'})
        metadata_fut = client.set_topics(('topic2', ))

        try:
            await asyncio.wait_for(
                metadata_fut,
                timeout=0.2
            )
        except asyncio.TimeoutError:
            pass

        self.assertFalse(client._sync_task.done())

        await coordinator.close()
        await client.close()
