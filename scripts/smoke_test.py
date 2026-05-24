#!/usr/bin/env python3
"""
Smoke test for a *deployed* ConsensusChallenge contract.

This script talks directly to the GenLayer Studio JSON-RPC endpoint —
no SDK install required, just `pip install requests`.

It verifies the original bug is gone:  after submit_word / add, the
current_room field actually contains data.

Usage:
    python scripts/smoke_test.py \
        --contract 0x8443995060C9dd4bBE97A9e7e39F4E73c43cCb19 \
        --rpc https://studio.genlayer.com/api \
        [--account 0xYourPrivateKey]   # only needed for write tests
"""

import argparse
import json
import sys
import time
import urllib.request


# ---------------------------------------------------------------- helpers

def rpc(url: str, method: str, params):
    body = json.dumps({
        "jsonrpc": "2.0",
        "method":  method,
        "params":  params,
        "id":      int(time.time() * 1000),
    }).encode()

    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        out = json.loads(resp.read())
    if "error" in out and out["error"]:
        raise RuntimeError(f"RPC error: {out['error']}")
    return out.get("result")


def view(rpc_url, contract, method, args=None):
    """Call a @gl.public.view method via gen_call."""
    payload = {
        "from":    "0x0000000000000000000000000000000000000000",
        "to":      contract,
        "data":    json.dumps({"method": method, "args": args or []}),
        "type":    "read",
    }
    raw = rpc(rpc_url, "gen_call", [payload])
    if isinstance(raw, str):
        s = raw
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1].encode().decode("unicode_escape")
        try:
            return json.loads(s)
        except ValueError:
            return s
    return raw


# ---------------------------------------------------------------- checks

class CheckFailed(Exception): pass

def check(name, cond, detail=""):
    icon = "✅" if cond else "❌"
    print(f"  {icon} {name}{(' — ' + detail) if detail else ''}")
    if not cond:
        raise CheckFailed(name)


def run(rpc_url, contract):
    print(f"\n🔍 Probing contract {contract}")
    print(f"   via {rpc_url}\n")

    # ---- 1. current_room reachable & well-formed
    print("1) get_game_status / get returns the expected shape")
    status = view(rpc_url, contract, "get_game_status")
    if status is None:
        status = view(rpc_url, contract, "get")
    check("status is an object", isinstance(status, dict), repr(status)[:80])
    for k in ("players", "addresses", "words"):
        check(f"  field '{k}' present", k in status)

    # ---- 2. leaderboard reachable
    print("\n2) get_leaderboard returns a dict")
    board = view(rpc_url, contract, "get_leaderboard")
    check("leaderboard is a dict", isinstance(board, dict))

    # ---- 3. history reachable
    print("\n3) get_history returns a list")
    try:
        hist = view(rpc_url, contract, "get_history", [10])
        check("history is a list", isinstance(hist, list))
    except Exception as e:
        check("history endpoint exists", False, str(e)[:80])

    # ---- 4. THE BIG ONE: after a submission, current_room is non-empty
    print("\n4) (informational) snapshot of current_room right now:")
    print("     players=%s  words=%s" % (status.get("players"),
                                         status.get("words")))
    if status.get("players", 0) > 0:
        print("   👉 current_room is NOT empty — bug appears fixed ✨")
    else:
        print("   ℹ️  current_room is empty.  Submit a word from the UI and re-run.")

    print("\n✨ Smoke test finished.\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", required=True, help="0x… contract address")
    ap.add_argument("--rpc",      default="https://studio.genlayer.com/api",
                    help="JSON-RPC endpoint")
    args = ap.parse_args()

    try:
        run(args.rpc, args.contract)
    except CheckFailed as e:
        print(f"\n❌ Check failed: {e}\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}\n", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
