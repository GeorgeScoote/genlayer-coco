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
    def submit_word(self, player: str, word: str) -> str:
        key = player.lower()
        room = json.loads(self.current_room)
        board = json.loads(self.leaderboard)
        
        room[key] = word.lower()
        if key not in board:
            board[key] = 0
        board[key] = board[key] + 20
        
        self.current_room = json.dumps(room)
        self.leaderboard = json.dumps(board)
        
        return json.dumps({"success": True, "xp": board[key]})

    @gl.public.write  
    def settle_game(self) -> str:
        room = json.loads(self.current_room)
        board = json.loads(self.leaderboard)
        
        if len(room) < 2:
            self.current_room = "{}"
            return json.dumps({"success": True})
        
        players_by_word = {}
        for player, word in room.items():
            if word not in players_by_word:
                players_by_word[word] = []
            players_by_word[word].append(player)
        
        for word, players in players_by_word.items():
            if len(players) >= 2:
                for p in players:
                    board[p] = board[p] + 50
        
        self.current_room = "{}"
        self.leaderboard = json.dumps(board)
        return json.dumps({"success": True})

    @gl.public.view
    def get_leaderboard(self) -> str:
        return self.leaderboard

    @gl.public.view
    def get_game_status(self) -> str:
        room = json.loads(self.current_room)
        return json.dumps({"players": len(room), "addresses": list(room.keys()), "words": list(room.values())})
