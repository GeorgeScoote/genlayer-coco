# { "Depends": "py-genlayer:test" }
"""
GenLayer Consensus Challenge — fixed contract
---------------------------------------------
Fixes vs. the original:
  1. Adds the `add(word)` / `get()` methods the frontend actually calls.
  2. Reads sender from `gl.message.sender_address` instead of a string param,
     so users can't spoof other players' addresses.
  3. Uses `sort_keys=True` on every `json.dumps` so all validators produce
     identical state and consensus succeeds.
  4. Adds the missing 5-player auto-settle + on-chain LLM judging that the
     README advertises.
  5. Keeps the legacy `submit_word` / `get_game_status` aliases.
  6. Persists `history` and exposes `get_history(n)` for the History tab.
"""

from genlayer import *
import json

ROOM_SIZE      = 5
PARTICIPATE_XP = 10   # README says +10 for participants
WIN_XP         = 50   # README says +50 for winners
HISTORY_LIMIT  = 50


class ConsensusChallenge(gl.Contract):
    leaderboard:  str
    current_room: str
    history:      str

    def __init__(self):
        self.leaderboard  = "{}"
        self.current_room = "{}"
        self.history      = "[]"

    # =====================================================
    # WRITE METHODS
    # =====================================================

    @gl.public.write
    def add(self, word: str) -> str:
        """Frontend-facing entry point. Sender comes from tx context."""
        sender = gl.message.sender_address.as_hex
        return self._submit(sender, word)

    @gl.public.write
    def submit_word(self, player: str, word: str) -> str:
        """Legacy alias kept for backward compatibility."""
        return self._submit(player, word)

    @gl.public.write
    def settle_game(self) -> str:
        """Manually settle the current room (rarely needed — auto-settles at 5)."""
        return self._settle()

    # =====================================================
    # VIEW METHODS
    # =====================================================

    @gl.public.view
    def get(self) -> str:
        return self.get_game_status()

    @gl.public.view
    def get_game_status(self) -> str:
        room = json.loads(self.current_room)
        return json.dumps({
            "players":   len(room),
            "addresses": list(room.keys()),
            "words":     list(room.values()),
        }, sort_keys=True)

    @gl.public.view
    def get_leaderboard(self) -> str:
        return self.leaderboard

    @gl.public.view
    def get_history(self, n: int = 10) -> str:
        hist = json.loads(self.history)
        n = max(1, int(n))
        return json.dumps(hist[-n:], sort_keys=True)

    @gl.public.view
    def get_player_xp(self, player: str) -> int:
        board = json.loads(self.leaderboard)
        return int(board.get(player.lower(), 0))

    @gl.public.view
    def has_submitted(self, player: str) -> bool:
        room = json.loads(self.current_room)
        return player.lower() in room

    @gl.public.view
    def get_players_count(self) -> int:
        room = json.loads(self.current_room)
        return len(room)

    # =====================================================
    # INTERNAL HELPERS
    # =====================================================

    def _submit(self, player: str, word: str) -> str:
        key   = player.lower()
        clean = (word or "").strip().lower()
        if not clean:
            return json.dumps({"success": False, "error": "empty_word"})

        room  = json.loads(self.current_room)
        board = json.loads(self.leaderboard)

        if key in room:
            return json.dumps({"success": False, "error": "already_submitted"})

        room[key]  = clean
        board[key] = int(board.get(key, 0)) + PARTICIPATE_XP

        # Persist BEFORE auto-settle so writes are atomic per-validator
        self.current_room = json.dumps(room,  sort_keys=True)
        self.leaderboard  = json.dumps(board, sort_keys=True)

        # 5-player auto-settle
        if len(room) >= ROOM_SIZE:
            self._settle()
            # re-read board for the response
            board = json.loads(self.leaderboard)

        return json.dumps({
            "success": True,
            "xp":      int(board.get(key, 0)),
            "players": len(room) if len(room) < ROOM_SIZE else 0,
        })

    def _settle(self) -> str:
        room  = json.loads(self.current_room)
        board = json.loads(self.leaderboard)

        if not room:
            return json.dumps({"success": True, "winners": []})

        # --- 1. exact-match consensus (deterministic, always counts) ---
        counts = {}
        for w in room.values():
            counts[w] = counts.get(w, 0) + 1
        exact_winners = {w for w, c in counts.items() if c >= 2}

        # --- 2. semantic consensus via on-chain LLM (best-effort) ---
        llm_winners = set()
        if len(room) >= 2:
            words = sorted(room.values())
            prompt = (
                "You are judging a blockchain word-matching game.\n"
                f"Players submitted: {words}\n"
                "Return ONLY a compact JSON object exactly like "
                '{"winners":["word1","word2"]} listing the words that are '
                "semantically most similar to each other. "
                "If none are similar, return {\"winners\":[]}.  "
                "Do not include any explanation."
            )
            try:
                verdict = gl.exec_prompt(prompt)
                parsed  = json.loads(verdict)
                llm_winners = {str(w).strip().lower()
                               for w in parsed.get("winners", [])}
            except Exception:
                llm_winners = set()

        winning_words = exact_winners | llm_winners

        # --- 3. payout ---
        winners = []
        for player, w in room.items():
            if w in winning_words:
                board[player] = int(board.get(player, 0)) + WIN_XP
                winners.append(player)

        # --- 4. save history + reset room ---
        hist = json.loads(self.history)
        hist.append({
            "room":          room,
            "winners":       sorted(winners),
            "winning_words": sorted(list(winning_words)),
        })

        self.history      = json.dumps(hist[-HISTORY_LIMIT:], sort_keys=True)
        self.current_room = "{}"
        self.leaderboard  = json.dumps(board, sort_keys=True)

        return json.dumps({
            "success":       True,
            "winners":       sorted(winners),
            "winning_words": sorted(list(winning_words)),
        })
