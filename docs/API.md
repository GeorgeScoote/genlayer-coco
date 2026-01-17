# Contract API Reference

## Contract Address

**Testnet:** `0xD4e85A9b3687817CdDBd481a05e238b77e57c79D`

---

## Write Methods

### submit_word

Submit a keyword to the current game room.

```python
submit_word(word: str) -> dict
```

**Parameters:**
- `word` (str): Blockchain-related keyword (max 50 chars)

**Returns:**
```json
{
  "success": true,
  "players": 3,
  "word": "consensus"
}
```

**Errors:**
- `Already submitted` - Player already in current room

---

## View Methods

### get_leaderboard

Get all players' XP scores.

```python
get_leaderboard() -> dict
```

**Returns:**
```json
{
  "0x1234...5678": 150,
  "0xabcd...ef12": 100
}
```

### get_player_xp

Get XP for a specific player.

```python
get_player_xp(address: str) -> int
```

**Returns:** Integer XP value

### get_players_count

Get current room player count.

```python
get_players_count() -> int
```

**Returns:** Integer (0-5)

### get_game_status

Get current game state.

```python
get_game_status() -> dict
```

**Returns:**
```json
{
  "players": 3,
  "addresses": ["0x123...", "0x456..."],
  "words": ["consensus", "validator"]
}
```

### get_history

Get recent game history.

```python
get_history(limit: int = 10) -> list
```

**Returns:**
```json
[
  {
    "id": 1,
    "players": ["0x123...", "0x456..."],
    "words": ["consensus", "validator"],
    "winners": ["0x123..."],
    "theme": "blockchain consensus"
  }
]
```

### has_submitted

Check if address has submitted in current round.

```python
has_submitted(address: str) -> bool
```

**Returns:** Boolean

---

## Events Flow

```
1. Player calls submit_word("consensus")
2. Contract stores word in current_room
3. When 5 players join:
   - AI analyzes semantic similarity
   - Winners get +50 XP
   - Others get +10 XP
   - Game history recorded
   - Room cleared
```
