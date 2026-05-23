# Tests

Two complementary test layers:

| File | Type | What it does |
|---|---|---|
| `test_consensus_challenge.py` | gltest unit | Spins up a fresh contract on a local GenLayer simulator for each test |
| `../scripts/smoke_test.py`    | RPC probe  | Hits an *already-deployed* contract via JSON-RPC, verifies the bug is gone |

## Running the gltest suite

```bash
# 0. Make sure a GenLayer Studio simulator is running locally
#    (see https://github.com/yeagerai/genlayer-studio)

# 1. Install test deps
pip install gltest genlayer-py pytest

# 2. From repo root
pytest tests/ -v
```

Expected output:

```
tests/test_consensus_challenge.py::test_initial_state_is_empty             PASSED
tests/test_consensus_challenge.py::test_single_submission_persists_current_room  PASSED
tests/test_consensus_challenge.py::test_cannot_submit_twice               PASSED
tests/test_consensus_challenge.py::test_five_submissions_trigger_auto_settle PASSED
tests/test_consensus_challenge.py::test_history_is_capped                 PASSED
tests/test_consensus_challenge.py::test_view_helpers                      PASSED
tests/test_consensus_challenge.py::test_sender_cannot_be_spoofed          PASSED
tests/test_consensus_challenge.py::test_empty_word_rejected               PASSED
```

The most important one is **`test_single_submission_persists_current_room`** —
that's the regression test for the original "current_room 始终没有填写" bug.

## Running the smoke test against testnet

```bash
python scripts/smoke_test.py \
    --contract 0xYourNewlyDeployedAddress \
    --rpc https://studio.genlayer.com/api
```
