# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

class ConsensusChallenge(gl.Contract):
    leaderboard: str
    current_room: str
    game_history: str
    current_theme: str

    def __init__(self, name: str):
        self.leaderboard = "{}"
        self.current_room = "{}"
        self.game_history = "[]"
        self.current_theme = "DeFi"

    @gl.public.write
    def submit_word(self, word: str) -> str:
        key = f"{gl.message.sender}"
        room = json.loads(self.current_room)
        board = json.loads(self.leaderboard)
        
        if key in room:
            return json.dumps({"success": False, "error": "Already submitted"})
        
        theme = self.current_theme
        
        # AI验证词语是否符合主题
        def validate_word():
            prompt = f"Is the word '{word}' related to {theme} in crypto/blockchain context? Answer only 'yes' or 'no'."
            result = gl.exec_prompt(prompt)
            return result.strip().lower() == "yes"
        
        is_valid = gl.eq_principle_strict_eq(validate_word)
        
        if not is_valid:
            return json.dumps({"success": False, "error": f"Word '{word}' not related to {theme} theme"})
        
        # 验证通过，记录词语
        room[key] = word.lower()
        if key not in board:
            board[key] = 0
        
        # 基础奖励 +20 XP
        board[key] = board[key] + 20
        
        self.current_room = json.dumps(room)
        self.leaderboard = json.dumps(board)
        return json.dumps({"success": True, "players": len(room), "validated": True})

    @gl.public.write
    def settle_game(self) -> str:
        room = json.loads(self.current_room)
        board = json.loads(self.leaderboard)
        history = json.loads(self.game_history)
        
        if len(room) < 2:
            return json.dumps({"success": False, "error": "Need at least 2 players"})
        
        # 统计词语
        words_list = list(set(room.values()))
        players_by_word = {}
        for player, word in room.items():
            if word not in players_by_word:
                players_by_word[word] = []
            players_by_word[word].append(player)
        
        theme = self.current_theme
        
        # AI投票选最佳词语
        def select_best_word():
            prompt = f"Which word best represents {theme} in crypto? Options: {words_list}. Return ONLY the word, nothing else."
            result = gl.exec_prompt(prompt)
            return result.strip().lower()
        
        best_word = gl.eq_principle_strict_eq(select_best_word)
        
        winners = []
        
        # 匹配奖励 +50 XP（2人以上相同词语）
        for word, players in players_by_word.items():
            if len(players) >= 2:
                for p in players:
                    board[p] = board[p] + 50
                    winners.append(p)
        
        # 冠军奖励 +100 XP（AI选中的最佳词语）
        if best_word in players_by_word:
            for p in players_by_word[best_word]:
                board[p] = board[p] + 100
        
        # 保存游戏历史
        history.append({
            "players": list(room.keys()),
            "words": list(room.values()),
            "winners": winners,
            "best_word": best_word,
            "theme": theme
        })
        
        # 清空房间
        self.current_room = "{}"
        self.leaderboard = json.dumps(board)
        self.game_history = json.dumps(history)
        
        return json.dumps({
            "success": True, 
            "settled": True, 
            "best_word": best_word,
            "winners": winners
        })

    @gl.public.write
    def set_theme(self, theme: str) -> str:
        self.current_theme = theme
        return json.dumps({"success": True, "theme": theme})

    @gl.public.view
    def get_game_status(self) -> str:
        room = json.loads(self.current_room)
        return json.dumps({
            "players": len(room),
            "addresses": list(room.keys()),
            "words": list(room.values()),
            "theme": self.current_theme
        })

    @gl.public.view
    def get_leaderboard(self) -> str:
        return self.leaderboard

    @gl.public.view
    def get_history(self) -> str:
        return self.game_history

    @gl.public.view
    def get_theme(self) -> str:
        return self.current_theme
