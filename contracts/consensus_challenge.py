from genlayer import *

@gl.contract
class ConsensusChallenge:
    # 永久存储 - 玩家XP
    leaderboard: PersistentDict[str, int]
    # 永久存储 - 游戏历史
    game_history: PersistentList[dict]
    # 当前房间玩家
    current_room: PersistentDict[str, str]  # address -> word
    # 游戏计数
    game_count: PersistentInt

    def __init__(self):
        self.leaderboard = PersistentDict()
        self.game_history = PersistentList()
        self.current_room = PersistentDict()
        self.game_count = PersistentInt(0)

    @gl.public.write
    def submit_word(self, word: str) -> dict:
        sender = gl.message.sender
        
        # 检查是否已提交
        if sender in self.current_room:
            return {"success": False, "error": "Already submitted"}
        
        # 记录提交
        self.current_room[sender] = word
        
        # 初始化玩家XP（如果新玩家）
        if sender not in self.leaderboard:
            self.leaderboard[sender] = 0
        
        # 检查房间是否满5人
        if len(self.current_room) >= 5:
            return self._settle_game()
        
        return {
            "success": True, 
            "players": len(self.current_room),
            "word": word
        }

    def _settle_game(self) -> dict:
        players = list(self.current_room.keys())
        words = [self.current_room[p] for p in players]
        
        # 使用 AI 分析语义相似度
        prompt = f"""Analyze these blockchain-related words and find the most semantically similar pair:
Words: {words}
Return JSON: {{"winners": ["word1", "word2"], "theme": "common theme"}}"""
        
        result = gl.exec_prompt(prompt)
        
        # 解析结果确定获胜者
        try:
            import json
            ai_result = json.loads(result)
            winning_words = ai_result.get("winners", words[:2])
            theme = ai_result.get("theme", "blockchain")
        except:
            winning_words = words[:2]
            theme = "blockchain"
        
        # 分配XP
        winners = []
        for i, player in enumerate(players):
            if words[i] in winning_words:
                self.leaderboard[player] += 50  # 获胜者 +50 XP
                winners.append(player)
            else:
                self.leaderboard[player] += 10  # 参与者 +10 XP
        
        # 记录历史
        self.game_count.set(self.game_count.get() + 1)
        self.game_history.append({
            "id": self.game_count.get(),
            "players": players,
            "words": words,
            "winners": winners,
            "theme": theme
        })
        
        # 清空房间
        self.current_room.clear()
        
        return {
            "success": True,
            "settled": True,
            "winners": winners,
            "theme": theme
        }

    @gl.public.view
    def get_leaderboard(self) -> dict:
        """返回所有玩家XP"""
        return dict(self.leaderboard)

    @gl.public.view
    def get_player_xp(self, address: str) -> int:
        """获取指定玩家XP"""
        return self.leaderboard.get(address, 0)

    @gl.public.view
    def get_players_count(self) -> int:
        """当前房间人数"""
        return len(self.current_room)

    @gl.public.view
    def get_game_status(self) -> dict:
        """获取当前游戏状态"""
        return {
            "players": len(self.current_room),
            "addresses": list(self.current_room.keys()),
            "words": list(self.current_room.values())
        }

    @gl.public.view
    def get_history(self, limit: int = 10) -> list:
        """获取最近游戏历史"""
        history = list(self.game_history)
        return history[-limit:] if len(history) > limit else history

    @gl.public.view
    def has_submitted(self, address: str) -> bool:
        """检查是否已提交"""
        return address in self.current_room
