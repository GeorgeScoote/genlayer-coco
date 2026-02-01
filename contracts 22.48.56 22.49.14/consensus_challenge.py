# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

class ConsensusChallenge(gl.Contract):
    leaderboard: str
    current_room: str

    def __init__(self, name: str):
        self.leaderboard = "{}"
        self.current_room = "{}"

    @gl.public.write
    def submit_word(self, word: str) -> str:
        sender = gl.message.sender
        room = json.loads(self.current_room)
        board = json.loads(self.leaderboard)
        
        if sender in room:
            return json.dumps({"success": False, "error": "Already submitted"})
        
        room[sender] = word
        if sender not in board:
            board[sender] = 0
        
        if len(room) >= 5:
            for p in room.keys():
                board[p] = board.get(p, 0) + 10
            self.current_room = "{}"
            self.leaderboard = json.dumps(board)
            return json.dumps({"success": True, "settled": True})
        
        self.current_room = json.dumps(room)
        self.leaderboard = json.dumps(board)
        return json.dumps({"success": True, "players": len(room)})

    @gl.public.view
    def get_game_status(self) -> str:
        room = json.loads(self.current_room)
        return json.dumps({
            "players": len(room),
            "addresses": list(room.keys()),
            "words": list(room.values())
        })

    @gl.public.view
    def get_leaderboard(self) -> str:
        return self.leaderboard
