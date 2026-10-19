import asyncio
import multiprocessing
from pathlib import Path
import time

import pytest

from hyperche.request_leases import RequestBroker, physical_key_id


def competing(path, output, key):
    broker = RequestBroker(path, total_limit=3)
    with broker.request(key, role="other-role", timeout=5):
        output.put(broker.stats()["active"])
        time.sleep(0.03)
    broker.close()


def abandoned(path):
    broker = RequestBroker(path)
    assert broker.try_acquire("synthetic-key", role="crashing-worker")


def test_mixed_process_roles_share_global_limit_and_key(tmp_path):
    path = str(tmp_path / "leases.sqlite")
    ctx = multiprocessing.get_context("spawn")
    output = ctx.Queue()
    workers = [ctx.Process(target=competing, args=(path, output, "key" + str(i % 4))) for i in range(8)]
    for worker in workers: worker.start()
    for worker in workers:
        worker.join(15)
        assert worker.exitcode == 0
    assert max(output.get(timeout=2) for _ in workers) <= 3
    broker = RequestBroker(path, total_limit=3)
    assert broker.stats() == {"requests": 8, "network_peak": 3, "key_peak": 1, "active": 0}
    assert b"synthetic-secret" not in Path(path).read_bytes()
    broker.close()


def test_same_key_does_not_get_extra_slot_from_different_role_or_limit(tmp_path):
    path = tmp_path / "leases.sqlite"
    one, other = RequestBroker(path, total_limit=1), RequestBroker(path, total_limit=10)
    with one.try_acquire("synthetic-secret", role="embedding"):
        assert other.try_acquire("synthetic-secret", role="normalization") is None
    with other.try_acquire("synthetic-secret", role="chat"):
        assert one.stats()["active"] == 1
    one.close()
    other.close()
    for file in tmp_path.glob("leases.sqlite*"):
        assert b"synthetic-secret" not in file.read_bytes()


def test_cancelled_wait_cannot_later_leak_a_slot(tmp_path):
    async def exercise():
        broker = RequestBroker(tmp_path / "leases.sqlite")
        lease = await broker.acquire("key", role="first")
        waiting = asyncio.create_task(broker.acquire("key", role="cancelled"))
        await asyncio.sleep(0.04)
        waiting.cancel()
        with pytest.raises(asyncio.CancelledError): await waiting
        lease.release()
        await asyncio.sleep(0.05)
        assert broker.stats()["active"] == 0
        broker.close()
    asyncio.run(exercise())


def test_dead_worker_reclaimed_but_live_worker_is_not_expired(tmp_path):
    path = str(tmp_path / "leases.sqlite")
    worker = multiprocessing.get_context("spawn").Process(target=abandoned, args=(path,))
    worker.start()
    worker.join(15)
    assert worker.exitcode == 0
    broker = RequestBroker(path)
    with broker.try_acquire("synthetic-key", role="resumed"):
        assert broker.stats()["active"] == 1
        broker.db.execute("UPDATE leases SET started=0")
        assert broker.try_acquire("synthetic-key", role="cannot-steal") is None
    broker.close()


@pytest.mark.parametrize("key", ["", "a\nb", "a,b", "a;b"])
def test_joined_keys_rejected(key):
    with pytest.raises(ValueError): physical_key_id(key)


def test_unrelated_database_is_never_modified(tmp_path):
    import sqlite3
    path = tmp_path / "other.sqlite"
    connection = sqlite3.connect(path)
    connection.execute("CREATE TABLE existing (value TEXT)")
    connection.commit()
    connection.close()
    before = path.read_bytes()
    with pytest.raises(ValueError, match="non-request-broker"): RequestBroker(path)
    assert path.read_bytes() == before
