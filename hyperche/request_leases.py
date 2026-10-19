"""Process-shared physical-key request leases for explicitly integrated clients.

The database contains SHA256 key fingerprints, never credentials. A live
process's lease is never stolen on a clock timeout. All request paths must use
this broker before claiming that an installation-wide limit is enforced.
"""
from __future__ import annotations

import asyncio
from contextlib import contextmanager
import ctypes
import hashlib
import os
from pathlib import Path
import sqlite3
import threading
import time
import uuid


def process_alive(pid: int) -> bool:
    if pid == os.getpid():
        return True
    if os.name == "nt":
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            # Access denied does not establish that a process is dead.
            return ctypes.get_last_error() == 5
        try:
            code = ctypes.c_ulong()
            if not kernel.GetExitCodeProcess(ctypes.c_void_p(handle), ctypes.byref(code)):
                return True
            return code.value == 259
        finally:
            kernel.CloseHandle(ctypes.c_void_p(handle))
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def physical_key_id(key: str) -> str:
    if not isinstance(key, str) or not key.strip() or any(c in key for c in "\r\n,;"):
        raise ValueError("One physical API key is required")
    return hashlib.sha256(key.strip().encode()).hexdigest()


class Lease:
    def __init__(self, broker, identifier):
        self.broker, self.id, self.released = broker, identifier, False

    def release(self):
        if not self.released:
            self.broker.release(self.id)
            self.released = True

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        self.release()


class RequestBroker:
    """One global <=10 actual requests and exactly one request per key.

    Endpoint/profile/role names deliberately do not partition the limit.
    Lower caller limits may further restrict active requests, never raise it.
    A lease is acquired immediately before transport and released in finally.
    """
    def __init__(self, path: str | Path | None = None, *, total_limit=10):
        if not isinstance(total_limit, int) or isinstance(total_limit, bool) or not 1 <= total_limit <= 10:
            raise ValueError("Global actual request limit must be between 1 and 10")
        self.total_limit = total_limit
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local/share")) / "HyperChE"
        self.path = Path(path) if path else base / "actual_request_leases.sqlite"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.db = sqlite3.connect(self.path, timeout=30, isolation_level=None, check_same_thread=False)
        tables = {row[0] for row in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if tables and "broker_meta" not in tables:
            self.db.close()
            raise ValueError("Refusing to initialize a non-request-broker database")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("CREATE TABLE IF NOT EXISTS broker_meta (version TEXT PRIMARY KEY)")
        self.db.execute("INSERT OR IGNORE INTO broker_meta VALUES ('physical-key-v1')")
        self.db.execute("CREATE TABLE IF NOT EXISTS leases (id TEXT PRIMARY KEY,key_hash TEXT UNIQUE,pid INTEGER,role TEXT,started REAL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS request_counts (id INTEGER PRIMARY KEY CHECK(id=1),requests INTEGER,network_peak INTEGER)")
        self.db.execute("INSERT OR IGNORE INTO request_counts VALUES (1,0,0)")

    def try_acquire(self, key: str, *, role: str) -> Lease | None:
        key_hash = physical_key_id(key)
        if not role or len(role) > 100:
            raise ValueError("A short non-secret role name is required")
        with self.lock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                for pid, in self.db.execute("SELECT DISTINCT pid FROM leases").fetchall():
                    if not process_alive(pid):
                        self.db.execute("DELETE FROM leases WHERE pid=?", (pid,))
                active = self.db.execute("SELECT COUNT(*) FROM leases").fetchone()[0]
                busy = self.db.execute("SELECT 1 FROM leases WHERE key_hash=?", (key_hash,)).fetchone()
                if busy or active >= self.total_limit:
                    self.db.execute("COMMIT")
                    return None
                identifier = uuid.uuid4().hex
                self.db.execute("INSERT INTO leases VALUES (?,?,?,?,?)",
                                (identifier, key_hash, os.getpid(), role, time.time()))
                self.db.execute("UPDATE request_counts SET requests=requests+1,network_peak=MAX(network_peak,?) WHERE id=1", (active + 1,))
                self.db.execute("COMMIT")
                return Lease(self, identifier)
            except BaseException:
                self.db.execute("ROLLBACK")
                raise

    async def acquire(self, key: str, *, role: str, timeout=600) -> Lease:
        deadline = time.monotonic() + timeout
        while True:
            lease = self.try_acquire(key, role=role)
            if lease:
                return lease
            if time.monotonic() >= deadline:
                raise TimeoutError("Actual request lease unavailable")
            await asyncio.sleep(0.02)

    @contextmanager
    def request(self, key: str, *, role: str, timeout=600):
        deadline = time.monotonic() + timeout
        while True:
            lease = self.try_acquire(key, role=role)
            if lease:
                break
            if time.monotonic() >= deadline:
                raise TimeoutError("Actual request lease unavailable")
            time.sleep(0.02)
        with lease:
            yield lease

    def release(self, identifier):
        with self.lock:
            self.db.execute("DELETE FROM leases WHERE id=? AND pid=?", (identifier, os.getpid()))

    def stats(self):
        with self.lock:
            requests, peak = self.db.execute("SELECT requests,network_peak FROM request_counts WHERE id=1").fetchone()
            active = self.db.execute("SELECT COUNT(*) FROM leases").fetchone()[0]
        return {"requests": requests, "network_peak": peak, "key_peak": 1 if requests else 0, "active": active}

    def close(self):
        self.db.close()
