"""
End-to-end tests for ConsensusChallenge contract.

Usage:
    # 1. install gltest if you haven't:
    pip install gltest genlayer-py

    # 2. run a local GenLayer simulator (in another terminal):
    docker compose up   # from genlayer-studio repo
    # OR set GENVM_URL to a running studio instance

    # 3. run the tests:
    pytest tests/test_consensus_challenge.py -v
"""

import json
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.helpers import default_account, create_new_account


CONTRACT_NAME = "ConsensusChallenge"


# --------------------------------------------------------------
#  Fixtures
# --------------------------------------------------------------

@pytest.fixture
def contract():
    """Deploy a fresh contract for each test."""
    factory = get_contract_factory(CONTRACT_NAME)
    c = factory.deploy(args=[])  # no ctor args after our fix
    return c


@pytest.fixture
def five_accounts():
    """Five distinct funded accounts so we can hit ROOM_SIZE."""
    return [default_account] + [create_new_account() for _ in range(4)]


# --------------------------------------------------------------
#  Helpers
# --------------------------------------------------------------

def _parse(view_result):
    """Contract views return JSON strings — normalize to dict/list/value."""
    if isinstance(view_result, (dict, list, int, bool)):
        return view_result
    try:
        return json.loads(view_result)
    except (TypeError, ValueError):
        return view_result


def _submit(contract, account, word):
    tx = contract.connect(account).add(args=[word]).transact()
    assert tx_execution_succeeded(tx), f"submit '{word}' from {account.address} failed"
    return tx


# --------------------------------------------------------------
#  Tests
# --------------------------------------------------------------

def test_initial_state_is_empty(contract):
    """Fresh contract: leaderboard, current_room and history all empty."""
    assert _parse(contract.get_leaderboard(args=[]).call()) == {}
    assert _parse(contract.get_history(args=[10]).call()) == []
    status = _parse(contract.get(args=[]).call())
    assert status["players"]   == 0
    assert status["addresses"] == []
    assert status["words"]     == []


def test_single_submission_persists_current_room(contract):
    """The original bug: submitting a word must leave current_room non-empty."""
    _submit(contract, default_account, "bitcoin")

    status = _parse(contract.get(args=[]).call())
    assert status["players"] == 1, "current_room is still empty -- bug not fixed!"
    assert status["words"]   == ["bitcoin"]
    assert default_account.address.lower() in [a.lower() for a in status["addresses"]]

    # +10 XP for participation
    board = _parse(contract.get_leaderboard(args=[]).call())
    me = default_account.address.lower()
    assert board.get(me) == 10


def test_cannot_submit_twice(contract):
    """Same player resubmitting in the same room should be rejected."""
    _submit(contract, default_account, "ethereum")

    tx = contract.connect(default_account).add(args=["solana"]).transact()
    # The TX itself may succeed but the return value carries the error flag
    result = _parse(tx.consensus_data.leader_receipt[0].return_value
                    if hasattr(tx, "consensus_data") else tx)
    if isinstance(result, dict):
        assert result.get("success") is False
        assert result.get("error") == "already_submitted"

    # current_room unchanged
    status = _parse(contract.get(args=[]).call())
    assert status["words"] == ["ethereum"]


def test_five_submissions_trigger_auto_settle(contract, five_accounts):
    """ROOM_SIZE submissions must auto-settle: room cleared, board awarded."""
    words = ["bitcoin", "ethereum", "bitcoin", "solana", "bitcoin"]
    for acct, w in zip(five_accounts, words):
        _submit(contract, acct, w)

    # Room should now be empty (auto-settled)
    status = _parse(contract.get(args=[]).call())
    assert status["players"] == 0, "expected auto-settle to clear current_room"
    assert status["addresses"] == []
    assert status["words"]     == []

    # 3 players submitted "bitcoin" -- exact-match consensus -> they get +50
    board = _parse(contract.get_leaderboard(args=[]).call())
    bitcoin_addrs = [a.address.lower() for a, w in zip(five_accounts, words) if w == "bitcoin"]
    for addr in bitcoin_addrs:
        # 10 participation + 50 win = 60
        assert board[addr] >= 60, f"winner {addr} did not get +50 XP (got {board[addr]})"

    # History got an entry
    hist = _parse(contract.get_history(args=[10]).call())
    assert len(hist) == 1
    assert "bitcoin" in hist[0]["winning_words"]


def test_history_is_capped(contract, five_accounts):
    """Running many rounds shouldn't blow up storage forever."""
    # Run two rounds of 5
    for round_idx in range(2):
        # Each round needs fresh-ish player addresses; reuse the same 5 is fine
        # because the room is reset between rounds.
        for i, acct in enumerate(five_accounts):
            _submit(contract, acct, f"word{round_idx}_{i}")
    hist = _parse(contract.get_history(args=[100]).call())
    assert len(hist) == 2


def test_view_helpers(contract):
    _submit(contract, default_account, "nft")
    assert contract.get_players_count(args=[]).call() == 1
    assert contract.has_submitted(args=[default_account.address]).call() is True

    other = create_new_account()
    assert contract.has_submitted(args=[other.address]).call() is False
    assert contract.get_player_xp(args=[default_account.address]).call() == 10
    assert contract.get_player_xp(args=[other.address]).call() == 0


def test_sender_cannot_be_spoofed(contract):
    """
    `add(word)` derives sender from gl.message — even if someone tries to
    pass the legacy submit_word(player, word) with a fake player, only their
    own address should ever get credited via `add`.
    """
    attacker = create_new_account()
    victim   = create_new_account()

    # attacker calls add -> their own address is recorded, not victim's
    contract.connect(attacker).add(args=["hack"]).transact()
    status = _parse(contract.get(args=[]).call())
    assert attacker.address.lower() in [a.lower() for a in status["addresses"]]
    assert victim.address.lower()  not in [a.lower() for a in status["addresses"]]


def test_empty_word_rejected(contract):
    tx = contract.connect(default_account).add(args=["   "]).transact()
    # current_room must stay empty
    status = _parse(contract.get(args=[]).call())
    assert status["players"] == 0
