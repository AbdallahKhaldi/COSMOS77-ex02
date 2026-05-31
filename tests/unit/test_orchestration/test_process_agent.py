"""AgentProcess: in-process worker coverage + a real spawned-process round-trip.

The real-process tests prove acceptance A1 (agent = separate OS process, IPC over
queues). No ``claude`` is invoked — a module-level FakeAgent stands in.
"""

from __future__ import annotations

import queue as queuemod
from types import SimpleNamespace

from cosmos77_ex02.agents.judge import JudgeAgent
from cosmos77_ex02.orchestration import process_agent as pa
from cosmos77_ex02.protocol.message import ProtocolMessage
from tests.unit.test_orchestration.helpers import build_fake_agent


def test_worker_processes_request_then_stops() -> None:
    inbound: queuemod.Queue = queuemod.Queue()
    outbound: queuemod.Queue = queuemod.Queue()
    heartbeat = SimpleNamespace(value=0.0)
    inbound.put({"method": "act", "kwargs": {"context": {"ping_no": 1}}})
    inbound.put(pa._STOP)
    pa._worker("pro", None, build_fake_agent, inbound, outbound, heartbeat)
    resp = outbound.get_nowait()
    assert resp["ok"] is True
    assert resp["result"].sender == "pro"
    assert heartbeat.value > 0


def test_worker_reports_agent_error() -> None:
    inbound: queuemod.Queue = queuemod.Queue()
    outbound: queuemod.Queue = queuemod.Queue()
    inbound.put({"method": "act", "kwargs": {}})  # FakeAgent.act needs a context arg
    inbound.put(pa._STOP)
    pa._worker("pro", None, build_fake_agent, inbound, outbound, SimpleNamespace(value=0.0))
    assert outbound.get_nowait()["ok"] is False


def test_build_default_agent_constructs_a_real_agent() -> None:
    assert isinstance(pa.build_default_agent("judge", None), JudgeAgent)


def test_real_process_round_trip() -> None:
    proc = pa.AgentProcess("pro", agent_builder=build_fake_agent)
    proc.start()
    try:
        msg = proc.call("act", timeout=20, context={"ping_no": 1, "turn_type": "opening"})
        assert isinstance(msg, ProtocolMessage)
        assert msg.sender == "pro" and msg.recipient == "judge"
        assert msg.citations == ["https://example.com/x"]
        assert proc.alive and proc.heartbeat_age() < 20
    finally:
        proc.terminate()
    assert not proc.alive


def test_real_process_restart() -> None:
    proc = pa.AgentProcess("con", agent_builder=build_fake_agent)
    proc.start()
    try:
        proc.restart()
        msg = proc.call("act", timeout=20, context={"ping_no": 2, "turn_type": "rebuttal"})
        assert msg.sender == "con"
    finally:
        proc.terminate()
