# GenLayer Consensus Challenge

A decentralized word-matching game built on GenLayer blockchain with AI-powered semantic analysis.

![GenLayer](https://img.shields.io/badge/GenLayer-Testnet-purple.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-green.svg)

## Overview

GenLayer Consensus Challenge is a multiplayer game where players submit blockchain-related keywords. The smart contract uses GenLayer's native LLM capabilities to analyze semantic similarity and determine winners.

**Live Contract:** `0xD4e85A9b3687817CdDBd481a05e238b77e57c79D`

## Features

- 🧠 **On-chain AI Analysis** - Semantic matching via `gl.exec_prompt`
- 💾 **Permanent Storage** - Leaderboard & history stored on-chain
- 🔗 **MetaMask Integration** - Direct wallet connection
- ⚡ **Real-time Updates** - Auto-refresh after transactions

## Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│                 │     │                      │     │                 │
│    Frontend     │────▶│   GenLayer Network   │────▶│  AI Validators  │
│    (HTML/JS)    │     │  (Smart Contract)    │     │   (LLM Nodes)   │
│                 │     │                      │     │                 │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

## Project Structure

```
genlayer-consensus-game/
├── contracts/
│   └── consensus_challenge.py   # GenLayer smart contract
├── frontend/
│   └── public/
│       └── index.html           # Game interface
├── docs/
│   ├── API.md                   # Contract API reference
│   └── DEPLOYMENT.md            # Deployment guide
├── scripts/
│   └── deploy.sh                # Deployment script
├── .env.example
├── .gitignore
├── LICENSE
├── package.json
└── README.md
```

## Quick Start

### Prerequisites

- Node.js 18+
- MetaMask wallet
- GenLayer CLI (`npm install -g genlayer`)

### Installation

```bash
git clone https://github.com/your-org/genlayer-consensus-game.git
cd genlayer-consensus-game
npm install
```

### Local Development

```bash
# Start local server
npm run dev

# Open http://localhost:3000
```

### Deploy Contract

```bash
# Deploy to GenLayer Testnet
npm run deploy
```

## Game Rules

| Step | Action | Reward |
|------|--------|--------|
| 1 | Connect MetaMask wallet | - |
| 2 | Submit a blockchain keyword | - |
| 3 | Wait for 5 players | - |
| 4 | AI analyzes semantic similarity | - |
| 5 | Winners (most similar words) | +50 XP |
| 6 | Participants | +10 XP |

## Contract API

### Write Methods

| Method | Parameters | Description |
|--------|------------|-------------|
| `submit_word` | `word: str` | Submit keyword to current game |

### View Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_leaderboard` | `dict` | All players' XP |
| `get_player_xp` | `int` | XP for specific address |
| `get_players_count` | `int` | Current room count |
| `get_game_status` | `dict` | Current game state |
| `get_history` | `list` | Recent game history |
| `has_submitted` | `bool` | Check submission status |

## Configuration

```env
# .env
VITE_CONTRACT_ADDRESS=0xD4e85A9b3687817CdDBd481a05e238b77e57c79D
VITE_RPC_URL=https://studio.genlayer.com/api
VITE_CHAIN_ID=61999
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Smart Contract | Python (GenLayer SDK) |
| Frontend | HTML5, Tailwind CSS, Vanilla JS |
| Blockchain | GenLayer Testnet |
| AI | GenLayer Native LLM |
| Wallet | MetaMask |

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push branch (`git push origin feature/amazing`)
5. Open Pull Request

## Resources

- [GenLayer Documentation](https://docs.genlayer.com)
- [GenLayer Studio](https://studio.genlayer.com)
- [GenLayer Discord](https://discord.gg/8Jm4v89VAu)

## License

MIT License - see [LICENSE](LICENSE)
